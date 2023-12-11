import itertools
from typing import List, Tuple

import numpy as np


def _expand_dimension(universe: np.array) -> np.array:  # noqa
    copy = []
    for i in range(len(universe)):
        copy.append(universe[i])
        if all(j == "." for j in universe[i]):
            copy.append(universe[i])

    return copy


def expand(universe: np.array) -> np.array:  # noqa
    copy = _expand_dimension(universe)
    copy = _expand_dimension(np.transpose(copy))
    return np.transpose(copy)


def search_galaxies(universe: np.array) -> List[Tuple[int, int]]:  # noqa
    result = []
    for i in range(len(universe)):
        for j in range(len(universe[i])):
            if universe[i][j] == "#":
                result.append((i, j))
    return result


def distance(g1: Tuple[int, int], g2: Tuple[int, int]) -> int:
    return abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        universe = [list(line.strip()) for line in f.readlines()]

    universe = expand(universe)
    galaxies = search_galaxies(universe)
    combinations = list(itertools.combinations(galaxies, 2))

    total = 0
    for c1, c2 in combinations:
        total += distance(c1, c2)

    print(total)
