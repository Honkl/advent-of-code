import re
import time
from multiprocessing import Pool
from typing import List, Tuple

import numpy as np


def is_valid(symbols: List[str], counts: List[int]) -> bool:
    pattern = "\\.+".join(f"#{{c}}".replace("c", str(c)) for c in counts)
    pattern = "^\\.*" + pattern + "\\.*$"
    return bool(re.search(pattern, "".join(symbols)))


def is_still_valid(symbols: List[str], counts: List[int]) -> bool:
    desired_count = counts[0]
    index = 0
    current_count = 0
    for i, ch in enumerate(symbols):
        if ch == ".":
            if current_count == 0:
                # Nothing found yet
                continue

            if current_count != desired_count:
                # We have more than we wanted
                # print(f"INVALID: {symbols}, {counts}")
                return False

            current_count = 0
            index += 1
            if index >= len(counts):
                desired_count = -1
            else:
                desired_count = counts[index]

        if ch == "#":
            current_count += 1

        if ch == "?":
            # Evaluate only till first question mark
            return True

    return True

    #
    # parts = "".join(symbols).split(".")
    # parts = [p for p in parts if p != ""]
    #
    # # We have complicated case, won't bother now lol
    # if len(parts) != len(counts):
    #     return True
    #
    # # Compare first count if it is still valid
    # for i, part in enumerate(parts):
    #     if part.count("#") > counts[i]:
    #         return False
    #
    # return True


def recursive_eval(symbols: List[str], counts: List[int]) -> int:
    if all(value != "?" for value in symbols):
        if is_valid(symbols, counts):
            # print(f"{symbols} <--- VALID")
            return 1
        # print(symbols)
        return 0

    if symbols.count("#") > sum(counts) or symbols.count("#") + symbols.count("?") < sum(counts):
        return 0

    if not is_still_valid(symbols, counts):
        return 0

    index = symbols.index("?")
    local_copy = symbols.copy()

    local_copy[index] = "."
    good = recursive_eval(local_copy, counts)

    local_copy[index] = "#"
    bad = recursive_eval(local_copy, counts)

    return good + bad


def evaluate(data: Tuple[str, List[int]]) -> int:  # noqa
    symbols, counts = data

    valid_combs = recursive_eval(list(symbols), counts)

    print(f"Combinations: {valid_combs}    {symbols}    {counts}")
    return valid_combs


def unfold(symbols: str, counts: List[int], k: int) -> Tuple[str, List[int]]:
    return "?".join([symbols] * k), list(np.array([counts] * k).flatten())


if __name__ == '__main__':

    with open("input.txt", "r") as f:
        springs, values = [], []
        for line in f:
            s, v = line.strip().split(" ")
            springs.append(s)
            values.append(list(map(int, v.split(","))))

    N = 3
    totals = []
    print("Evaluating unfolded results")
    for n in range(1, N + 1):
        start = time.time()
        data = [unfold(springs[i], values[i], n) for i in range(len(springs))]
        with Pool(16) as p:
            results = p.map(evaluate, data)

        totals.append(results)
        # print(sum(results))
        # print(time.time() - start)

    print("Totals:")
    for t in totals:
        print(t)

    print("Factors")
    factors = [b / a for a, b in zip(totals[0], totals[1])]
    print(factors)

    N = 5
    total = 0
    initials = totals[0]
    # print(initials)
    for value, factor in zip(initials, factors):
        multiplied = value * (factor ** (N - 1))
        # print(value, factor, multiplied)
        total += multiplied

    print(total)

