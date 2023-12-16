import numpy as np


def search_reflection(pattern: np.array) -> int:  # noqa
    for line_index in range(len(pattern)):
        up = pattern[:line_index]
        down = pattern[line_index:]

        if len(up) == 0:
            continue

        if len(up) < len(down):
            down = down[:len(up)]

        if len(up) > len(down):
            up = up[len(up) - len(down):]

        if all((a == b).all() for a, b in zip(up, down[::-1])):  # noqa
            return line_index

    return 0


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
        horizontal_score = search_reflection(p)
        vertical_score = search_reflection(np.transpose(p))

        total += vertical_score + 100 * horizontal_score

    print(total)
