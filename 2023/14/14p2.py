import itertools
from copy import deepcopy
from enum import Enum
from typing import List

import numpy as np


class Direction(Enum):
    LEFT = "L"
    RIGHT = "R"
    UP = "U"
    DOWN = "D"


def transpose(field: List) -> List:
    field = np.transpose(np.array(np.array([list(x) for x in field])))
    return ["".join(x) for x in field]


def tilt(field: List, direction: Direction) -> List:
    """
    Tilts the field and returns it after processing all rocks. Up and Down tilting directions are processed through
    transpose.
    """
    field = deepcopy(field)
    transpose_back = False
    if direction in [Direction.UP, Direction.DOWN]:
        field = transpose(field)
        direction = Direction.LEFT if direction == Direction.UP else Direction.RIGHT
        transpose_back = True

    result = []
    for row in field:
        shifted_groups = []
        hard_groups = [g for g in row.replace("O", ".").split(".") if g != ""]

        for soft_groups in [g for g in row.split("#") if g != ""]:
            rocks = soft_groups.count("O")
            empty = soft_groups.count(".")

            new_g = ("O" * rocks) + ("." * empty) if direction == Direction.LEFT else ("." * empty) + ("O" * rocks)
            shifted_groups.append(new_g)

        new_row = ""
        for soft, hard in list(itertools.zip_longest(shifted_groups, hard_groups, fillvalue="")):
            new_row += hard + soft if row[0] == "#" else soft + hard
        result.append(new_row)

    if transpose_back:
        return transpose(result)
    return result


def get_load(field: List) -> int:
    return sum([(len(field) - i) * field[i].count("O") for i in range(len(field))])


def cycle(field: List) -> List:
    tilted = tilt(field, Direction.UP)
    tilted = tilt(tilted, Direction.LEFT)
    tilted = tilt(tilted, Direction.DOWN)
    return tilt(tilted, Direction.RIGHT)


def cycle_length(sequence: List[int]) -> int:
    max_len = int(len(sequence) / 2)
    for x in range(2, max_len):
        if sequence[0:x] == sequence[x:2 * x]:
            return x
    return 1


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        data = [line.strip() for line in f]

    loads = []
    final = None
    iterations = 0
    target = 1_000_000_000

    while final is None:
        # Run another cycle
        cycled = cycle(data)
        loads.append(get_load(cycled))
        iterations += 1

        # Evaluate if the sequence started to cycle itself
        # Remove initial elements to find, if the sequence started to cycle from some point
        for i in range(len(loads)):
            cycle_len = cycle_length(loads[i:])

            # We found cyclic behaviour in loads sequences
            if cycle_len > 1:
                # Cyclic dependency starts at index "i" -> interpolate for target index
                index = (target - i - 1) % cycle_len

                # Pick modulo-ed index (+ starting value, where the cyclic dependency starts)
                final = loads[index + i]
                break

        data = cycled

    print(final)
