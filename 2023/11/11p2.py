import itertools
from typing import List, Tuple

import numpy as np


def _expand_dimension(universe: np.array) -> np.array:  # noqa
    copy = []
    for i in range(len(universe)):
        if all(j in [".", "I"] for j in universe[i]):
            copy.append(["I"] * len(universe[i]))
        else:
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
    if g1 == g2:
        return 0
    crosses = 0
    for i in range(min(g1[0], g2[0]), max(g1[0], g2[0])):
        if universe[i][1] == "I":
            crosses += 1

    for i in range(min(g1[1], g2[1]), max(g1[1], g2[1])):
        if universe[0][i] == "I":
            crosses += 1

    dist = abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
    expand_factor = (crosses * 1_000_000) - crosses
    return dist + expand_factor


with open("input.txt", "r") as f:
    universe = [list(line.strip()) for line in f.readlines()]

universe = expand(universe)
galaxies = search_galaxies(universe)
combinations = list(itertools.product(galaxies, galaxies))

if __name__ == '__main__':

    total = 0
    for c in combinations:
        total += distance(c[0], c[1])

    print(total / 2)
