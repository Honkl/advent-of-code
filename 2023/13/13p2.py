import numpy as np  # noqa
import copy
from typing import Optional


def swap(pattern: np.array, i: int, j: int) -> np.array:  # noqa
    cp = copy.deepcopy(pattern)
    cp[i][j] = "#" if pattern[i][j] == "." else "."
    return cp


def search_reflection(pattern: np.array, reflection_line: Optional[int]) -> int:  # noqa
    reflections = []
    for line_index in range(len(pattern)):
        up = pattern[:line_index]
        down = pattern[line_index:]

        if len(up) == 0 or len(up) == len(pattern):
            continue

        if len(up) < len(down):
            down = down[:len(up)]

        if len(up) > len(down):
            up = up[len(up) - len(down):]

        if all((a == b).all() for a, b in zip(up, down[::-1])):  # noqa
            reflections.append(line_index)

    if len(reflections) == 0:
        return 0

    if len(reflections) == 1:
        return reflections[0]

    assert len(reflections) == 2, reflections

    # Return "the other" reflection (the newly found)
    return reflections[0] if reflections[1] == reflection_line else reflections[1]


if __name__ == '__main__':

    patterns = []
    with open("input.txt", "r") as f:

        pattern = []
        for line in f:
            if line.strip() == "":
                patterns.append(np.array(pattern))
                pattern = []
                continue
            pattern.append(np.array([ch for ch in line.strip()]))
        patterns.append(pattern)

    total = 0
    for p in patterns:
        # Original score
        horizontal_score = search_reflection(p, None)
        vertical_score = search_reflection(np.transpose(p), None)

        fixed = False
        for i in range(len(p)):
            if fixed:
                break
            for j in range(len(p[i])):
                swap_p = swap(p, i, j)
                new_horizontal_score = search_reflection(swap_p, horizontal_score)
                new_vertical_score = search_reflection(np.transpose(swap_p), vertical_score)

                # Same reflection, we try another swap
                if horizontal_score == new_horizontal_score and vertical_score == new_vertical_score:
                    continue

                # We found new vertical reflection
                if new_vertical_score > 0 and new_vertical_score != vertical_score:
                    total += new_vertical_score
                    fixed = True
                    break

                # We found new horizontal reflection
                if new_horizontal_score > 0 and new_horizontal_score != horizontal_score:
                    total += 100 * new_horizontal_score
                    fixed = True
                    break

    print(total)
