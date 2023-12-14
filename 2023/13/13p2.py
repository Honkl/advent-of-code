import numpy as np  # noqa
import copy


def swap(pattern: np.array, i: int, j: int) -> np.array:  # noqa
    cp = copy.deepcopy(pattern)
    cp[i][j] = "#" if pattern[i][j] == "." else "."
    return cp


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
    for x, p in enumerate(patterns):

        print(x)

        fixed = False
        for i in range(len(p)):
            if fixed:
                break
            for j in range(len(p[i])):
                horizontal_score = search_reflection(p)
                vertical_score = search_reflection(np.transpose(p))

                # print(p)
                swap_p = swap(p, i, j)
                # print(p)

                new_horizontal_score = search_reflection(swap_p)
                new_vertical_score = search_reflection(np.transpose(swap_p))

                # print(horizontal_score, vertical_score, new_horizontal_score, new_vertical_score)

                if horizontal_score == new_horizontal_score and vertical_score == new_vertical_score:
                    # print(i, j)
                    continue

                if new_vertical_score > 0 and new_vertical_score != vertical_score:
                    print(
                        f"i={i}, j={j}, vs={vertical_score}, new_vs={new_vertical_score}, hs={horizontal_score}, new_hs={new_horizontal_score}")
                    total += new_vertical_score
                    fixed = True
                    break

                if new_horizontal_score > 0 and new_horizontal_score != horizontal_score:
                    print(
                        f"i={i}, j={j}, vs={vertical_score}, new_vs={new_vertical_score}, hs={horizontal_score}, new_hs={new_horizontal_score}")
                    total += 100 * new_horizontal_score
                    fixed = True
                    break

        if not fixed:
            if horizontal_score > 0:
                total += 100 * horizontal_score
            if vertical_score > 0:
                total += vertical_score
            print("WTF")
    print(total)
