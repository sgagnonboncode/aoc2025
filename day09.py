from functools import cache
from src.file_utils import read_example_input, read_input
from src.merry import display_splash_title
from enum import Enum
from colorama import Fore, Back, Style
from tqdm import tqdm
from src.grids import TupleGrid2D
from PIL import Image, ImageDraw

PUZZLE_ID = 9
display_splash_title(PUZZLE_ID)

# input = read_example_input(PUZZLE_ID)
input = read_input(PUZZLE_ID)

class Position2D(tuple[int, int]):
    @property
    def x(self) -> int:
        return self[0]

    @property
    def y(self) -> int:
        return self[1]
       
class Rectangle:
    def __init__(self, pos1: Position2D, pos2: Position2D):
        self.min_x = min(pos1.x, pos2.x)
        self.max_x = max(pos1.x, pos2.x)
        self.min_y = min(pos1.y, pos2.y)
        self.max_y = max(pos1.y, pos2.y)

    def area(self) -> int:
        return (self.max_x - self.min_x + 1) * (self.max_y - self.min_y + 1)

positions = list(map(Position2D, (tuple(map(int, line.strip().split(","))) for line in input)))


all_rectangles: list[Rectangle] = [Rectangle(positions[-1], positions[0])]

for i in range(0, len(positions) - 1):
    for j in range(i + 1, len(positions)):
        rect = Rectangle(positions[i], positions[j])
        all_rectangles.append(rect)

all_rectangles = sorted(all_rectangles, key=lambda r: r.area(), reverse=True)
part1 = all_rectangles[0].area()



# this method was left in the codebase to regenerate the visualization of tiles
# should you need to see it again. it will not be used in the actual solution.
# invoke it to use the day09viz.html file to visualize the area.
# def output_shape(positions: list[Position2D], filename_prefix: str= "day09_tile_"):
#     # the following code section genrates image tiles for visualization of the area.
#     # this was mixed with a web page to visualize the area. the idea was to determine if the
#     # 'polyline' described by the input created enclosed areas, which it didnt.

#     class TileType(Enum):
#         UNKNOWN = 0
#         RED = 1
#         GREEN = 2
#         UNAVAILABLE = 3

#     tile_grid = TupleGrid2D[TileType]()

#     # fill the grid with red tiles
#     for pos in positions:
#         tile_grid[(pos.x, pos.y)] = TileType.RED

#     # fill the borders with green tiles
#     for i in range(0,len(positions)):
#         cur = positions[i]
#         next = positions[i+1] if i+1 < len(positions) else positions[0]

#         # determine the orientation of the segment
#         if cur.x == next.x:
#             # vertical segment
#             x = cur.x
#             y_start = min(cur.y, next.y)
#             y_end = max(cur.y, next.y)
#             for y in range(y_start+1, y_end):
#                 if (x, y) not in tile_grid:
#                     tile_grid[(x, y)] = TileType.GREEN
#         elif cur.y == next.y:
#             # horizontal segment
#             y = cur.y
#             x_start = min(cur.x, next.x)
#             x_end = max(cur.x, next.x)
#             for x in range(x_start+1, x_end):
#                 if (x, y) not in tile_grid:
#                     tile_grid[(x, y)] = TileType.GREEN


#     tile_size = 5000  # each tile will be 5000x5000 pixels

#     (min_x, min_y), (max_x, max_y) = tile_grid.get_bounds()
#     # using PIL, create a series of 5000x5000 bitmap and print the tiles_grid on them
#     nb_tiles_x = (max_x - min_x) // tile_size + 1
#     nb_tiles_y = (max_y - min_y) // tile_size + 1

#     for tile_x in range(0, nb_tiles_x):
#         for tile_y in range(0, nb_tiles_y):
#             img = Image.new("RGB", (tile_size, tile_size), color=(0, 0, 0))
#             draw = ImageDraw.Draw(img)

#             # initialize the image to black
#             draw.rectangle([0, 0, tile_size, tile_size], fill=(0, 0, 0))
        
#             # for each position in the tile, draw the corresponding tile
#             all_set_tiles = tile_grid.keys()
#             for pos in all_set_tiles:
#                 global_x = pos[0]
#                 global_y = pos[1]

#                 if global_x < min_x + tile_x * tile_size or global_x >= min_x + (tile_x + 1) * tile_size:
#                     continue
#                 if global_y < min_y + tile_y * tile_size or global_y >= min_y + (tile_y + 1) * tile_size:
#                     continue

#                 local_x = global_x - (min_x + tile_x * tile_size)
#                 local_y = global_y - (min_y + tile_y * tile_size)

#                 tile_type = tile_grid[(global_x, global_y)]
#                 if tile_type == TileType.RED:
#                     color = (255, 0, 0)
#                 elif tile_type == TileType.GREEN:
#                     color = (0, 255, 0)
#                 else:
#                     color = (0, 0, 0)

#                 draw.rectangle([local_x, local_y, local_x+1, local_y+1], fill=color)

#             img.save(f"{filename_prefix}{tile_x}_{tile_y}.png")

# uncomment to generate the tile images for day09 visualization
# output_shape(positions)


#  the resulting shape is (very!) roughly:
#
#         ############
#       ##----------- ##
#      # |           |   #
#      # |   ???     |    #  (edges are very jagged in the actual shape)
#     #  |           |    ##
#     #  |           |     ##
#     ################      #
#        P A C M A N #     ##
#     ################    ##
#     #                  ##
#      #                #
#       #              #
#        ##############
#
# I have settled on calling it a PACMAN-like shape, since is almost a circle 
#  with a rectangular mouth opened to the left.
#
# since we know that the line never crosses itself , we will instead represent
# the area as a polyline of segments. positions which are 'INSIDE' the polyline will be considered
# either Green or Red (does not matter for part2)
#
# we will then test the best rectangles defined in part 1 against this polyline
# to determine if any edge of the rectangle crosses the polyline until we find one that fits,
# going from the biggest to the smallest.
#
# NOTE: this algorithm does NOT account and will return a false positive for the special case 
#       where the tested rectangle is in the 'mouth' of the pacman shape. (four corners of the mouth)
#       The reason for that is that the area is question is very small compared to the rest of the shape
#       (the proportions in the shape above are not accurate; that rectangle is actually very narrow).
#       I did not implement it because finding a bigger rectangle before reaching it was pretty much 
#       a given by definition of my puzzle input. my solution may or may not work for other inputs.
part2=0
for rect in all_rectangles:
    # test if any segment crosses inside of the rectangle
    crosses = False
    for i in range(0,len(positions)):
        cur = positions[i]
        next = positions[i+1] if i+1 < len(positions) else positions[0]

        # determine the orientation of the segment
        if cur.x == next.x:
            # vertical segment
            x = cur.x
            y_start = min(cur.y, next.y)
            y_end = max(cur.y, next.y)

            if y_end <= rect.min_y or y_start >= rect.max_y:
                # segment is above or below the rectangle,
                continue

            if x == rect.min_x or x == rect.max_x:
                continue  # segment is on the edge of the rectangle

            if rect.min_x < x < rect.max_x:
                crosses = True
                break  # segment crosses the rectangle

        elif cur.y == next.y:
            # horizontal segment
            y = cur.y
            x_start = min(cur.x, next.x)
            x_end = max(cur.x, next.x)

            if x_end <= rect.min_x or x_start >= rect.max_x:
                continue  # segment is left or right of the rectangle

            if y == rect.min_y or y == rect.max_y:
                continue  # segment is on the edge of the rectangle
            
            if rect.min_y < y < rect.max_y:
                crosses = True
                break  # segment crosses the rectangle
 
    if not crosses:
        print(f"Found rectangle at ({rect.min_x},{rect.min_y}) to ({rect.max_x},{rect.max_y})")
        part2 = rect.area()
        break

print(f"{Fore.GREEN}Part 1: {Fore.RESET} {part1}")
print(f"{Fore.GREEN}Part 2: {Fore.RESET} {part2}")
