from src.file_utils import read_example_input, read_input
from src.merry import display_splash_title
from enum import Enum
from colorama import Fore, Back, Style

PUZZLE_ID = 1
display_splash_title(PUZZLE_ID)

position = 50
password_part1 = 0
password_part2 = 0

input = read_input(PUZZLE_ID)
# input = read_example_input(PUZZLE_ID)

for line in input:
    if not line or len(line) < 2:
        continue

    l_r = 0
    if line[0] == "R":
        l_r = 1
    elif line[0] == "L":
        l_r = -1

    clicks = int(line[1:])

    while clicks > 100:
        clicks -= 100
        password_part2 += 1

    started_at_zero = position == 0
    position = position + l_r * clicks

    if position < 0:
        position += 100
        if position != 0 and not started_at_zero:
            password_part2 += 1
    elif position >= 100:
        position -= 100
        if position != 0 and not started_at_zero:
            password_part2 += 1

    if position == 0:
        password_part1 += 1
        password_part2 += 1

print(f"{Fore.GREEN}Part 1: {Fore.RESET} {password_part1}")
print(f"{Fore.GREEN}Part 2: {Fore.RESET} {password_part2}")
