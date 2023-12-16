import sys
from enum import Enum

sys.setrecursionlimit(10 ** 6)


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


MAP = {
    ".": {
        Direction.UP: [Direction.UP],
        Direction.DOWN: [Direction.DOWN],
        Direction.LEFT: [Direction.LEFT],
        Direction.RIGHT: [Direction.RIGHT],
    },
    "|": {
        Direction.UP: [Direction.UP],
        Direction.DOWN: [Direction.DOWN],
        Direction.LEFT: [Direction.UP, Direction.DOWN],
        Direction.RIGHT: [Direction.UP, Direction.DOWN],
    },
    "-": {
        Direction.UP: [Direction.LEFT, Direction.RIGHT],
        Direction.DOWN: [Direction.LEFT, Direction.RIGHT],
        Direction.LEFT: [Direction.LEFT],
        Direction.RIGHT: [Direction.RIGHT],
    },
    "/": {
        Direction.UP: [Direction.RIGHT],
        Direction.DOWN: [Direction.LEFT],
        Direction.LEFT: [Direction.DOWN],
        Direction.RIGHT: [Direction.UP],
    },
    "\\": {
        Direction.UP: [Direction.LEFT],
        Direction.DOWN: [Direction.RIGHT],
        Direction.LEFT: [Direction.UP],
        Direction.RIGHT: [Direction.DOWN],
    },
}

with open("input.txt", "r") as f:
    data = [list(row.strip()) for row in f]

history = {}


def light(i: int, j: int, direction: Direction) -> None:
    if i < 0 or j < 0 or i > len(data) - 1 or j > len(data[i]) - 1:
        return

    key = f"{i}-{j}"

    # We already have light passing from this direction into this cell
    if key in history.keys():
        if direction in history[key]:
            return
    else:
        history[key] = [direction]

    symbol = data[i][j]
    for outbound_direction in MAP[symbol][direction]:
        new_i = i
        new_j = j
        if outbound_direction == direction.DOWN:
            new_i = i + 1
        elif outbound_direction == direction.UP:
            new_i = i - 1
        elif outbound_direction == direction.RIGHT:
            new_j = j + 1
        elif outbound_direction == direction.LEFT:
            new_j = j - 1

        light(new_i, new_j, outbound_direction)


if __name__ == '__main__':
    light(0, 0, Direction.RIGHT)
    print(len(history.keys()))
