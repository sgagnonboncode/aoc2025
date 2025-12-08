from functools import cache
from src.file_utils import read_example_input, read_input
from src.merry import display_splash_title
from enum import Enum
from colorama import Fore, Back, Style
from tqdm import tqdm

PUZZLE_ID = 6
display_splash_title(PUZZLE_ID)

# input = read_example_input(PUZZLE_ID)
input = read_input(PUZZLE_ID)


class Operator(Enum):
    ADD = "+"
    MUL = "*"


class MathProblem:
    def __init__(self, operator: Operator, columns: int):
        self.normal_operands: list[int] = []
        self.cephalopod_operands: list[list[int]] = [[] for _ in range(columns)]
        self.operator: Operator = operator

    def add_operand(self, value: int):
        self.normal_operands.append(value)

    def add_cephalopod_digit(self, column: int, digit: int):
        self.cephalopod_operands[column].append(digit)

    def evaluate(self) -> int:
        if self.operator == Operator.ADD:
            return sum(self.normal_operands)
        elif self.operator == Operator.MUL:
            result = 1
            for op in self.normal_operands:
                result *= op
            return result
        else:
            raise ValueError("Unknown operator")

    def evaluate_cephalopod(self) -> int:
        # build the operands from the digits
        operands = []
        for digit_list in self.cephalopod_operands:
            operand_value = 0
            for digit in digit_list:
                operand_value = operand_value * 10 + digit
            operands.append(operand_value)

        # do the cephalopod math
        # normally we would have to reverse the operands list
        #  to respect the 'cephalopod' order, but since
        #  addition and multiplication are commutative,
        #  we can skip that step here.
        if self.operator == Operator.ADD:
            result = sum(operands)
        elif self.operator == Operator.MUL:
            result = 1
            for op in operands:
                result *= op
        else:
            raise ValueError("Unknown operator")

        # print(f"Cephalopod operands: {operands} Operator: {self.operator} Result: {result}")
        return result


# parse the positions of the operators from the last line
problems: list[MathProblem] = []
operators_pos: list[int] = []
operators_value: list[Operator] = []

for i, op in enumerate(input[-1]):
    if op in ("+", "*"):
        operators_pos.append(i)
        operators_value.append(Operator.ADD if op == "+" else Operator.MUL)

for i in range(0, len(operators_pos) - 1):
    next_pos = operators_pos[i + 1]
    column_count = next_pos - operators_pos[i] - 1
    problems.append(MathProblem(operators_value[i], column_count))

# scan the largest line to determine the number of columns for the last problem
max_line_length = max(len(line) for line in input)
last_operator_columns = max_line_length - operators_pos[-1] - 1
problems.append(MathProblem(operators_value[-1], last_operator_columns))

# map digit positions/columns to problems to avoid
# having to re-scan the operators for each new line
digit_problem_map: dict[int, tuple[int, int]] = {}
for i in range(max_line_length):
    # first problem
    if i < operators_pos[0]:
        digit_problem_map[i] = (0, i)
        continue
    # middle problems
    for j, op_pos in enumerate(operators_pos):
        if i < op_pos:
            column = i - (0 if j == 0 else operators_pos[j - 1] + 1)
            digit_problem_map[i] = (j - 1, column)
            break
    # last problem
    else:
        digit_problem_map[i] = (len(problems) - 1, i - operators_pos[-1] - 1)


for line in input[0:-1]:
    # normal operands, split by spaces
    tokens = line.split()
    for i, token in enumerate(tokens):
        problems[i].add_operand(int(token))

    # cephalopod operands
    # scan the line one character at a time, adding digits as we find them
    for i, d in enumerate(line):
        if d.isdigit():
            digit_value = int(d)
            problem_nb, column = digit_problem_map[i]
            problems[problem_nb].add_cephalopod_digit(column, digit_value)

part1 = sum(p.evaluate() for p in problems)
part2 = sum(p.evaluate_cephalopod() for p in problems)

print(f"{Fore.GREEN}Part 1: {Fore.RESET} {part1}")
print(f"{Fore.GREEN}Part 2: {Fore.RESET} {part2}")
