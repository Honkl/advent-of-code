import timeit
from enum import Enum


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


def penalty(d1: Direction, d2: Direction) -> int:
    return 0 if d1 == d2 else 1000


def search(i: int, j: int, d: Direction, min_cost: int) -> int:
    visited = {}
    stack = [(i, j, d, 0)]

    while len(stack) > 0:
        i, j, d, cost = stack.pop(0)

        if grid[i][j] == "E":
            if cost < min_cost:
                min_cost = cost
            continue

        if any([
            grid[i][j] == "#",
            cost > min_cost,
            (i, j) in visited and visited[(i, j)] < cost,
        ]):
            continue

        visited[(i, j)] = cost
        stack.append((i - 1, j, Direction.UP, cost + 1 + penalty(d, Direction.UP)))
        stack.append((i + 1, j, Direction.DOWN, cost + 1 + penalty(d, Direction.DOWN)))
        stack.append((i, j - 1, Direction.LEFT, cost + 1 + penalty(d, Direction.LEFT)))
        stack.append((i, j + 1, Direction.RIGHT, cost + 1 + penalty(d, Direction.RIGHT)))

    return min_cost


if __name__ == '__main__':
    start = timeit.default_timer()

    grid = []
    start_i, start_j = 0, 0
    with open("input.txt", "r") as f:
        for row_i, line in enumerate(f):
            grid.append(list(line.strip()))

            if "S" in line:
                start_i = row_i
                start_j = line.index("S")

    result = search(start_i, start_j, Direction.RIGHT, min_cost=10 ** 9)

    print(f"Cost: {result}")
    print(f"Runtime: {timeit.default_timer() - start}s")
