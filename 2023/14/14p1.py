import itertools
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


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        data = [line.strip() for line in f]

    tilted = tilt(data, Direction.UP)

    load = sum([(len(tilted) - i) * tilted[i].count("O") for i in range(len(tilted))])

    print(load)
