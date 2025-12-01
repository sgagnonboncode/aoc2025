def read_lines(path) -> list[str]:
    with open(path, "r") as f:
        return f.readlines()


def read_input(puzzle_id: int) -> list[str]:
    path = f"input/day{puzzle_id:02d}/input.txt"
    return read_lines(path)


def read_example_input(puzzle_id: int) -> list[str]:
    path = f"input/day{puzzle_id:02d}/example.txt"
    return read_lines(path)
