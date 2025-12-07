from functools import cache
from src.file_utils import read_example_input, read_input
from src.merry import display_splash_title
from enum import Enum
from colorama import Fore, Back, Style
from tqdm import tqdm
from src.grids import TupleGrid2D

PUZZLE_ID = 7
display_splash_title(PUZZLE_ID)

# input = read_example_input(PUZZLE_ID)
input = read_input(PUZZLE_ID)

grid = TupleGrid2D[str]()
tachyon_grid = TupleGrid2D[int]()

for y, line in enumerate(input):
    for x, char in enumerate(line.strip()):
        grid[(x, y)] = char
        tachyon_grid[(x, y)] = 0

start_pos = None
for x in range(len(input[0])):
    if grid[(x, 0)] == 'S':
        start_pos = (x, int(0))
        break

if start_pos is None:
    raise ValueError("Start position 'S' not found in the first line")

tachyon_grid[start_pos] = 1

bounds = grid.get_bounds()
min_x, min_y = bounds[0]
max_x, max_y = bounds[1]

part1=0
for y in range(min_y+1, max_y + 1):
    row = grid.get_row(y)
    previous_row = grid.get_row(y-1)

    for i, char in enumerate(previous_row):
        beams = tachyon_grid[(i, y-1)]
        if beams >0:
            if row[i] == '.':
                grid[(i, y)] = '|'
                tachyon_grid[(i, y)] += beams
            elif row[i] == '^':
                part1 += 1
                # left
                if i-1 >= min_x and row[i-1] == '.':
                        grid[(i-1, y)] = '|'
                        tachyon_grid[(i-1, y)] += beams
                # right
                if i+1 <= max_x and row[i+1] == '.':
                        grid[(i+1, y)] = '|'
                        tachyon_grid[(i+1, y)] += beams


# for y in range(min_y, max_y + 1):
#     row = grid.get_row(y)
#     print(''.join(row))

# for y in range(min_y, max_y + 1):
#     row = tachyon_grid.get_row(y)
#     print(' '.join(f"{v:2}" for v in row))

part2 = sum(tachyon_grid.get_row(max_y))

print(f"{Fore.GREEN}Part 1: {Fore.RESET} {part1}")
print(f"{Fore.GREEN}Part 2: {Fore.RESET} {part2}")
