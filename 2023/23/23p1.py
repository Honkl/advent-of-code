import sys
from enum import Enum
from typing import List

sys.setrecursionlimit(10 ** 9)

with open("input.txt", "r") as f:
    data = [list(line.strip()) for line in f]


class Direction(Enum):
    L = "L"
    R = "R"
    U = "U"
    D = "D"


def step(
        i: int, j: int, target_i: int, target_j: int, source_direction: Direction, steps: int, visited: List[str]
) -> int:
    key = f"{i}-{j}"
    if key in visited:
        return 0

    new_visited = visited.copy() + [key]

    if i == target_i and j == target_j:
        return steps

    try:
        symbol = data[i][j]
    except:  # noqa
        return 0

    options = []
    if symbol == ">" and source_direction == Direction.R:
        options.append(step(i, j + 1, target_i, target_j, source_direction, steps + 1, new_visited))
    if symbol == "<" and source_direction == Direction.L:
        options.append(step(i, j - 1, target_i, target_j, source_direction, steps + 1, new_visited))
    if symbol == "^" and source_direction == Direction.U:
        options.append(step(i - 1, j, target_i, target_j, source_direction, steps + 1, new_visited))
    if symbol == "v" and source_direction == Direction.D:
        options.append(step(i + 1, j, target_i, target_j, source_direction, steps + 1, new_visited))
    if symbol == ".":
        options.append(step(i + 1, j, target_i, target_j, Direction.D, steps + 1, new_visited))
        options.append(step(i - 1, j, target_i, target_j, Direction.U, steps + 1, new_visited))
        options.append(step(i, j + 1, target_i, target_j, Direction.R, steps + 1, new_visited))
        options.append(step(i, j - 1, target_i, target_j, Direction.L, steps + 1, new_visited))

    if len(options) == 0:
        return 0

    return max(options)


if __name__ == '__main__':
    final_i = len(data) - 1
    final_j = len(data[-1]) - 2
    print(f"Starting position: {final_i, final_j, data[final_i][final_j]}")

    result = step(0, 1, final_i, final_j, Direction.D, 0, [])
    print(result)
