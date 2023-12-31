import itertools
import re
from typing import List


def is_valid(symbols: str, counts: List[int]) -> bool:
    pattern = "\\.+".join(f"#{{c}}".replace("c", str(c)) for c in counts)
    pattern = "\\.*" + pattern + "\\.*"
    return bool(re.search(pattern, "".join(symbols)))


def evaluate(symbols: str, counts: List[int]) -> int:
    unknown_indices = []
    failed = 0
    for j in range(len(symbols)):
        if symbols[j] == "?":
            unknown_indices.append(j)
        if symbols[j] == "#":
            failed += 1

    # This amount of failed needs to be allocated
    unknown_failed = sum(counts) - failed

    valid_combs = 0
    for combination in itertools.combinations(unknown_indices, unknown_failed):
        spring = list(symbols)
        for index in combination:
            spring[index] = "#"

        spring = "".join(spring).replace("?", ".")  # Remaining indices

        if is_valid(spring, counts):
            valid_combs += 1

    return valid_combs


if __name__ == '__main__':

    total = 0

    with open("input.txt", "r") as f:
        for line in f:
            s, c = line.strip().split(" ")
            c = list(map(int, c.split(",")))
            total += evaluate(s, c)

    print(total)
