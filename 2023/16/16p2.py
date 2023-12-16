import sys
from enum import Enum
from typing import List

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


def get_energy(i: int, j: int, direction: Direction) -> int:
    light(i, j, direction)
    e = len(history.keys())
    history.clear()
    return e


if __name__ == '__main__':
    max_energy = 0
    options = []

    options.extend([(i, 0, Direction.RIGHT) for i in range(len(data))])
    options.extend([(i, -1, Direction.LEFT) for i in range(len(data))])
    options.extend([(0, j, Direction.DOWN) for j in range(len(data[0]))])
    options.extend([(-1, j, Direction.UP) for j in range(len(data[-1]))])

    for i, j, d in options:
        energy = get_energy(i, j, d)
        if energy > max_energy:
            max_energy = energy

    print(max_energy)
