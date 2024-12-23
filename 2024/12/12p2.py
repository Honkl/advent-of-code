import timeit
from typing import Optional
from enum import StrEnum


class Direction(StrEnum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


def compute_region(row: int, col: int, grid: list[list[str]]) -> Optional[list[tuple[int, int]]]:
    """Computes single region for provided starting position."""

    # This position has been already visited as part of different region
    if grid[row][col] == "#":
        return None

    stack = [(row, col)]
    visited = []
    while len(stack) > 0:
        i, j = stack.pop()

        if (i, j) in visited:
            continue

        visited.append((i, j))

        # Up
        if i - 1 >= 0 and grid[i][j] == grid[i - 1][j]:
            stack.append((i - 1, j))

        # Down
        if i + 1 < len(grid) and grid[i][j] == grid[i + 1][j]:
            stack.append((i + 1, j))

        # Left
        if j - 1 >= 0 and grid[i][j] == grid[i][j - 1]:
            stack.append((i, j - 1))

        # Right
        if j + 1 < len(grid[i]) and grid[i][j] == grid[i][j + 1]:
            stack.append((i, j + 1))

        grid[i][j] = "#"

    return visited


def solve_position(i: int, j: int, direction: Direction, sides: list) -> None:
    """Inplace update of `sides` list."""
    added = False
    for side in sides:

        a, b = (0,), (0,)
        match direction:
            case Direction.UP | Direction.DOWN:
                a = (i, j - 1)
                b = (i, j + 1)
            case Direction.LEFT | Direction.RIGHT:
                a = (i - 1, j)
                b = (i + 1, j)

        a = (a[0], a[1], direction)
        b = (b[0], b[1], direction)

        if a in side or b in side:
            side.append((i, j, direction))
            added = True

    if not added:
        sides.append([(i, j, direction)])


def eval_perimeter(region: list[tuple[int, int]], grid: list[list[str]]) -> int:
    """Build up all sides for the region."""
    sides = []
    for i, j in sorted(region):

        if i == 0 or (i - 1, j) not in region:
            solve_position(i, j, Direction.UP, sides)

        if i == len(grid) - 1 or (i + 1, j) not in region:
            solve_position(i, j, Direction.DOWN, sides)

        if j == 0 or (i, j - 1) not in region:
            solve_position(i, j, Direction.LEFT, sides)

        if j == len(grid[i]) - 1 or (i, j + 1) not in region:
            solve_position(i, j, Direction.RIGHT, sides)

    return len(sides)


def run() -> None:
    grid = []
    with open("input.txt", "r") as f:
        for line in f:
            grid.append(list(line.strip()))

    regions = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            visited = compute_region(i, j, grid)
            if visited:
                regions.append(visited)

    total = 0

    for i, region in enumerate(regions):
        area = len(region)
        p = eval_perimeter(region, grid)
        total += area * p
        print(f"{area} x {p} = {area * p}")

    print(f"Total: {total}")


if __name__ == '__main__':
    start = timeit.default_timer()
    run()
    print(f"Runtime: {timeit.default_timer() - start}s")
