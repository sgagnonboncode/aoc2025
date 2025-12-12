from src.file_utils import read_example_input, read_input
from src.merry import display_splash_title
from colorama import Fore, Back, Style
from tqdm import tqdm
import re
from z3 import Int, Sum, sat, Optimize
from functools import lru_cache
import time
import multiprocessing as mp
from multiprocessing import Pool


PUZZLE_ID = 12
display_splash_title(PUZZLE_ID)

# input = read_example_input(PUZZLE_ID)
input = read_input(PUZZLE_ID)

shapes : list[list[bool]] = []
current_shape : list[bool] = []

tree_zones : list[tuple[int,int]] = []
tree_shape_counts: list[list[int]] = []

for i,line in enumerate(input):
    line = line.strip()

    if i>=30:

        if i==30:
            shapes.append(current_shape)
            current_shape = []

        # list of areas
        # print(f"Processing line {i} for tree zones: {line}")
        l_r = line.split(": ")
        pos = l_r[0].split("x")
        tree_zones.append((int(pos[0]), int(pos[1])))
        tree_shape_counts.append([int(x) for x in l_r[1].split(" ")])


    else:
        # shapes
        if i%5 ==0 and i>0:
            if current_shape:
                shapes.append(current_shape)
                current_shape = []
        elif 0<i%5<4:
            # positions
            current_shape.extend([c == "#" for c in line[0:3]])

# calculate the number of open spaces in each shape
open_spaces_per_shape = []
for shape in shapes:
    open_spaces = sum(1 for cell in shape if not cell)
    open_spaces_per_shape.append(open_spaces)

NB_SHAPES = len(shapes)

# Cache rotated shape coordinates for performance
@lru_cache(maxsize=None)
def get_rotated_coords(shape_id: int, rotation: int) -> list[tuple[int, int]]:
    shape = shapes[shape_id]
    coords = []
    for y in range(3):
        for x in range(3):
            if shape[y*3 + x]:
                if rotation == 0:
                    coords.append((x, y))
                elif rotation == 1:  # 90 degrees
                    coords.append((2 - y, x))
                elif rotation == 2:  # 180 degrees
                    coords.append((2 - x, 2 - y))
                elif rotation == 3:  # 270 degrees
                    coords.append((y, 2 - x))
    return coords

def test_fitting(shape_id:int, rotation:int, current_grid:dict[tuple[int,int],bool], offset_x:int, offset_y:int) -> bool:
    coords = get_rotated_coords(shape_id, rotation)
    for rel_x, rel_y in coords:
        grid_x = offset_x + rel_x
        grid_y = offset_y + rel_y
        if current_grid[(grid_x, grid_y)]:
            return False
    return True



def apply_shape(shape_id:int, rotation:int, current_grid:dict[tuple[int,int],bool], offset_x:int, offset_y:int, debug_grid:dict[tuple[int,int],str] | None = None):
    coords = get_rotated_coords(shape_id, rotation)
    for rel_x, rel_y in coords:
        grid_x = offset_x + rel_x
        grid_y = offset_y + rel_y
        current_grid[(grid_x, grid_y)] = True
        if debug_grid:
            debug_grid[(grid_x, grid_y)] = f"{shape_id}"

def undo_shape(shape_id:int, rotation:int, current_grid:dict[tuple[int,int],bool], offset_x:int, offset_y:int, debug_grid:dict[tuple[int,int],str] | None = None):
    coords = get_rotated_coords(shape_id, rotation)
    for rel_x, rel_y in coords:
        grid_x = offset_x + rel_x
        grid_y = offset_y + rel_y
        current_grid[(grid_x, grid_y)] = False
        if debug_grid:
            debug_grid[(grid_x, grid_y)] = "."

def initialize_grid(width:int, height:int) -> dict[tuple[int,int],bool]:
    grid : dict[tuple[int,int],bool] = {}
    for y in range(height):
        for x in range(width):
            grid[(x,y)] = False
    return grid
def initialize_debug_grid(width:int, height:int) -> dict[tuple[int,int],str]:
    grid : dict[tuple[int,int],str] = {}
    for y in range(height):
        for x in range(width):
            grid[(x,y)] = "."
    return grid

def print_grid(debug_grid:dict[tuple[int,int],str], width:int, height:int):
    for y in range(height):
        row = ""
        for x in range(width):
            row += debug_grid[(x,y)]
        print(row)
    print("")

def process_zone(args):
    """Worker function to process a single zone"""
    i, zone, shape_counts = args
    
    area_available = zone[0] * zone[1]
    minimum_spaces_needed = sum(shape_counts[j] * (9-open_spaces_per_shape[j]) for j in range(len(shapes)))
    
    if minimum_spaces_needed > area_available:
        return i, False, f"Zone at {zone} cannot fit all trees. Minimum spaces needed: {minimum_spaces_needed}, available: {area_available}"

    grid = initialize_grid(zone[0], zone[1])
    debug_grid = initialize_debug_grid(zone[0], zone[1])
    
    # using backtracking, try to fit the shapes into the grid
    shapes_to_place = []
    for j in range(NB_SHAPES):
        for k in range(shape_counts[j]):
            shapes_to_place.append(j)
    
    # Sort shapes by difficulty (fewer open spaces = harder to place)
    shapes_to_place.sort(key=lambda s: open_spaces_per_shape[s])
    
    # Track iterations for timeout
    stats = {'iteration_count': 0, 'start_time': time.time()}
    MAX_ITERATIONS = 1000000
    TIMEOUT_SECONDS = 30
    
    def backtrack(place_index:int) -> bool:
        stats['iteration_count'] += 1
        
        # Early termination conditions
        if stats['iteration_count'] > MAX_ITERATIONS:
            return False
        if time.time() - stats['start_time'] > TIMEOUT_SECONDS:
            return False

        if place_index >= len(shapes_to_place):
            return True

        # try to place one of the remaining shapes
        next_shape_idx = shapes_to_place[place_index]
        
        # Try positions in a more systematic way (corners and edges first)
        positions = []
        # Corners first
        for y in range(min(3, zone[1]-2)):
            for x in range(min(3, zone[0]-2)):
                positions.append((x, y))
        # Then systematic grid search
        for y in range(zone[1]-2):
            for x in range(zone[0]-2):
                if (x, y) not in positions:
                    positions.append((x, y))
        
        for x, y in positions:
            for rotation in range(4):
                if test_fitting(next_shape_idx, rotation, grid, x, y):
                    # place the shape
                    apply_shape(next_shape_idx, rotation, grid, x, y, debug_grid)
                    if backtrack(place_index + 1):
                        return True
                    # undo the shape
                    undo_shape(next_shape_idx, rotation, grid, x, y, debug_grid)
        return False
    
    success = backtrack(0)
    if success:
        return i, True, f"Zone at {zone} can fit all presents."
    else:
        return i, False, f"Zone at {zone} cannot fit all presents."

if __name__ == '__main__':
    part1 = 0
    
    # Prepare arguments for multiprocessing
    zone_args = [(i, tree_zones[i], tree_shape_counts[i]) for i in range(len(tree_zones))]
    
    # Use multiprocessing with 12 cores
    with Pool(processes=12) as pool:
        # Process zones in parallel and print results as they come in
        for i, success, message in pool.imap_unordered(process_zone, zone_args):
            print(message)
            if success:
                part1 += 1




    print(f"{Fore.GREEN}Part 1: {Fore.RESET} {part1}")
    print(f"{Fore.GREEN}Part 2: SANTA GAVE ME A FREE STAR !")
