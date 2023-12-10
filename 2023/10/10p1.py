from enum import Enum
from typing import Tuple, List
import sys

sys.setrecursionlimit(10 ** 6)

with open("input.txt", "r") as f:
    field = [line.strip() for line in f]


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    @staticmethod
    def all_directions() -> List["Direction"]:
        return [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]


valid_entry_points = {
    "|": [Direction.UP, Direction.DOWN],
    "-": [Direction.LEFT, Direction.RIGHT],
    "L": [Direction.DOWN, Direction.LEFT],
    "J": [Direction.DOWN, Direction.RIGHT],
    "7": [Direction.UP, Direction.RIGHT],
    "F": [Direction.UP, Direction.LEFT],
    ".": [],
}

outbound_directions = {
    "|": {Direction.UP: Direction.UP, Direction.DOWN: Direction.DOWN},
    "-": {Direction.LEFT: Direction.LEFT, Direction.RIGHT: Direction.RIGHT},
    "L": {Direction.DOWN: Direction.RIGHT, Direction.LEFT: Direction.UP},
    "J": {Direction.DOWN: Direction.LEFT, Direction.RIGHT: Direction.UP},
    "7": {Direction.UP: Direction.LEFT, Direction.RIGHT: Direction.DOWN},
    "F": {Direction.UP: Direction.RIGHT, Direction.LEFT: Direction.DOWN},
    ".": [],
}


def is_valid(symbol: str, direction: Direction) -> bool:
    return direction in valid_entry_points[symbol]


def follow(i: int, j: int, start_i: int, start_j: int, direction: Direction, depth: int) -> Tuple[bool, int]:
    # Back to the original starting location
    if i == start_i and j == start_j:
        return True, depth

    try:
        symbol = field[i][j]
    except:  # noqa
        return False, depth

    if not is_valid(symbol, direction):
        return False, depth

    next_direction = outbound_directions[symbol][direction]
    if next_direction == Direction.UP:
        return follow(i - 1, j, start_i, start_j, next_direction, depth + 1)
    if next_direction == Direction.DOWN:
        return follow(i + 1, j, start_i, start_j, next_direction, depth + 1)
    if next_direction == Direction.LEFT:
        return follow(i, j - 1, start_i, start_j, next_direction, depth + 1)
    if next_direction == Direction.RIGHT:
        return follow(i, j + 1, start_i, start_j, next_direction, depth + 1)


def get_start() -> Tuple[int, int]:
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == "S":
                return i, j


if __name__ == '__main__':
    ii, jj = get_start()
    print(f"Starting location={ii}:{jj}")
    for dr in Direction.all_directions():
        next_ii, next_jj = ii, jj
        if dr == Direction.UP:
            next_ii = ii - 1
        if dr == Direction.DOWN:
            next_ii = ii + 1
        if dr == Direction.LEFT:
            next_jj = next_jj - 1
        if dr == Direction.RIGHT:
            next_jj = jj + 1

        loop = follow(next_ii, next_jj, ii, jj, dr, 1)
        print(f"Start direction={dr}, Loop={loop}, Length={loop[1] / 2}")
