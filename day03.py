from functools import cache
from src.file_utils import read_example_input, read_input
from src.merry import display_splash_title
from enum import Enum
from colorama import Fore, Back, Style
from tqdm import tqdm

PUZZLE_ID = 3
display_splash_title(PUZZLE_ID)

input = read_input(PUZZLE_ID)
# input = read_example_input(PUZZLE_ID)

part1 = 0
part2 = 0


def part_1_maximum_joltage(cells: list[int]) -> int:
    max_jolt = 0

    for i in range(0, len(cells) - 1):
        for j in range(i + 1, len(cells)):
            jolt = cells[i] * 10 + cells[j]
            if jolt > max_jolt:
                max_jolt = jolt
    return max_jolt


def part_2_compute_joltage(cells: list[int]) -> int:
    joltage = 0
    for v in cells:
        joltage = joltage * 10 + v
    return joltage


def part_2_maximum_joltage(cells: list[int]) -> int:
    # find the maximum number of cells by
    # discarding cells until only 12 remain.
    # solve using a number of passes until we
    #  can no longer prune.
    current = cells.copy()
    while len(current) > 12:
        removed_something = False

        # first pass : prune from the left
        cur = 0
        while len(current) > 12 and cur < len(current) - 1:
            if current[cur + 1] > current[cur]:
                current.pop(cur)
                removed_something = True
                break
            else:
                cur += 1

        if removed_something:
            removed_something = False
            continue

        # second pass : prune from the right, in case
        #  the tail end is high
        cur = len(current) - 1
        while len(current) > 12 and cur > 0:
            if current[cur - 1] > current[cur]:
                current.pop(cur)
                removed_something = True
                break
            cur -= 1

        if not removed_something:
            # no more pruning possible
            break

    # compute using the 12 leftmost cells.
    # (the only way we can have more than 12 is if we have something like all 9s)
    return part_2_compute_joltage(current[:12])


for line in input:
    cell_joltages = list(map(int, list(line.strip())))
    part1 += part_1_maximum_joltage(cell_joltages)
    part2 += part_2_maximum_joltage(cell_joltages)

print(f"{Fore.GREEN}Part 1: {Fore.RESET} {part1}")
print(f"{Fore.GREEN}Part 2: {Fore.RESET} {part2}")
