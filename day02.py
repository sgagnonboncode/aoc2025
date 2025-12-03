from src.file_utils import read_example_input, read_input
from src.merry import display_splash_title
from enum import Enum
from colorama import Fore, Back, Style

PUZZLE_ID = 2
display_splash_title(PUZZLE_ID)

input = read_input(PUZZLE_ID)
# input = read_example_input(PUZZLE_ID)

sequences = input[0].strip().split(",")


def test_part1_rule(id: str):
    if len(id) % 2 != 0:
        # by definition , the id is valid
        return True

    # test that the first half is different than the second half
    half = len(id) // 2
    return id[:half] != id[half:]


def test_part2_rule(id: str):
    # look for any sequence of repetition
    seq_len = 1
    while seq_len <= len(id) // 2:
        # ensure that the pattern can be repeated exactly
        if len(id) % seq_len != 0:
            seq_len += 1
            continue

        difference_found = False
        pattern = id[0:seq_len]

        cur = seq_len
        while cur + seq_len <= len(id):
            next = id[cur : cur + seq_len]
            if next != pattern:
                difference_found = True
                break
            cur += seq_len
        if not difference_found:
            return False

        seq_len += 1

    return True


part1 = 0
part2 = 0
for seq in sequences:
    start, stop = seq.split("-")
    for i in range(int(start), int(stop) + 1):
        id_str = str(i)
        if not test_part1_rule(id_str):
            part1 += i
        if not test_part2_rule(id_str):
            part2 += i

print(f"{Fore.GREEN}Part 1: {Fore.RESET} {part1}")
print(f"{Fore.GREEN}Part 2: {Fore.RESET} {part2}")
