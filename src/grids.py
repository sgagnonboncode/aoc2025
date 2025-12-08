from typing import Generic
from typing import TypeVar

T = TypeVar("T")


class TupleGrid2D(Generic[T], dict[tuple[int, int], T]):
    def get_row(self, y: int) -> list[T]:
        """Get all values in a specific row (y coordinate)"""
        row_values: list[T] = []
        x = 0
        while (x, y) in self:
            row_values.append(self[(x, y)])
            x += 1
        return row_values

    def get_column(self, x: int) -> list[T]:
        """Get all values in a specific column (x coordinate)"""
        col_values: list[T] = []
        y = 0
        while (x, y) in self:
            col_values.append(self[(x, y)])
            y += 1
        return col_values

    def get_bounds(self) -> tuple[tuple[int, int], tuple[int, int]]:
        """Get the bounds of the grid as ((min_x, min_y), (max_x, max_y))"""
        if not self:
            return ((0, 0), (0, 0))

        xs = set(coord[0] for coord in self.keys())
        ys = set(coord[1] for coord in self.keys())
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        return ((min_x, min_y), (max_x, max_y))
