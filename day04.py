from functools import cache
from src.file_utils import read_example_input, read_input
from src.merry import display_splash_title
from enum import Enum
from colorama import Fore, Back, Style
from tqdm import tqdm

PUZZLE_ID = 4
display_splash_title(PUZZLE_ID)

# input = read_example_input(PUZZLE_ID)
input = read_input(PUZZLE_ID)

class MapPosition(tuple[int,int]):
    @property
    def x(self) -> int:
        return self[0]
    @property
    def y(self) -> int:
        return self[1]

rolls:set[MapPosition] = set()

for y,line in enumerate(input):
    for x,char in enumerate(line.strip()):
        if char == '@':
            rolls.add(MapPosition((x,y)))


adjacent_offsets = [(-1,-1), (0,-1), (1,-1),
                    (-1,0),         (1,0),
                    (-1,1),  (0,1),  (1,1)]

MOVE_ROLL_THRESHOLD = 4

initial_nb_rolls = len(rolls)
first_step = True
while True:

    removable = set()

    for roll in rolls:
        nb_adjacent = 0
        for offset in adjacent_offsets:
            neighbor = MapPosition((roll.x + offset[0], roll.y + offset[1]))
            if neighbor in rolls:
                nb_adjacent += 1

        if nb_adjacent < MOVE_ROLL_THRESHOLD:            
            removable.add(roll)

    if first_step:
        part1 = len(removable)
        first_step = False

    if len(removable) == 0:
        break

    rolls = rolls.difference(removable)

part2 = initial_nb_rolls - len(rolls)

print(f"{Fore.GREEN}Part 1: {Fore.RESET} {part1}")
print(f"{Fore.GREEN}Part 2: {Fore.RESET} {part2}")
