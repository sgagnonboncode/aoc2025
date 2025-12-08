from functools import cache
from src.file_utils import read_example_input, read_input
from src.merry import display_splash_title
from enum import Enum
from colorama import Fore, Back, Style
from tqdm import tqdm

PUZZLE_ID = 5
display_splash_title(PUZZLE_ID)

# input = read_example_input(PUZZLE_ID)
input = read_input(PUZZLE_ID)


class FreshRange(tuple[int, int]):
    @property
    def start(self) -> int:
        return self[0]

    @property
    def end(self) -> int:
        return self[1]

    def contains(self, value: int) -> bool:
        return self.start <= value <= self.end


freshness_ranges: list[FreshRange] = []
range_completed = False

part1 = 0
part2 = 0

for line in input:
    if line.strip() == "":
        range_completed = True
        continue

    if not range_completed:
        parts = line.strip().split("-")
        freshness_ranges.append(FreshRange((int(parts[0]), int(parts[1]))))
    else:
        ingredient_id = int(line.strip())
        # evaluate freshness
        for range in freshness_ranges:
            if range.contains(ingredient_id):
                part1 += 1
                break

# part 2 : enumerate all possible freshness values
# we will not be testing all values one by one because
# doing so would take too long given the absurdly large
# ranges we have to deal with.
#
# instead , we will calculate the number of values thusly: 'end'-'start'+1
# then, we will substract any overlaps between ranges to avoid double counting.
#
# this can be easily done by sorting the ranges by start value, then iterating
# through them while keeping track of the last 'end' value we have seen.
freshness_ranges.sort(key=lambda r: r.start)
current_end = -1
for range in freshness_ranges:
    start = max(range.start, current_end + 1)
    end = range.end
    if end >= start:
        part2 += end - start + 1
        current_end = end


print(f"{Fore.GREEN}Part 1: {Fore.RESET} {part1}")
print(f"{Fore.GREEN}Part 2: {Fore.RESET} {part2}")
