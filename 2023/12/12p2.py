import os
import re
import time
from multiprocessing import Pool
from typing import List, Tuple

# Custom cache can be replaced with itertools built-in cache
cache = {}


def is_valid(symbols: List[str], counts: List[int]) -> bool:
    """
    Regex evaluation whether the specified pattern is valid with regards the counts.
    """
    pattern = "\\.+".join(f"#{{c}}".replace("c", str(c)) for c in counts)
    pattern = "^\\.*" + pattern + "\\.*$"
    return bool(re.search(pattern, "".join(symbols)))


def is_still_valid(symbols: List[str], counts: List[int]) -> bool:
    """
    Helper function that evaluates whether the `symbols` sequence can still match the `counts`. Returns False
    if we know at this point that it won't matter, what we will for remaining '?' at this point.

    We will count #s until first '?' and we will match it to first `counts` value.
    """
    if len(counts) == 0:
        return True

    desired_count = counts[0]
    index = 0
    current_count = 0
    for i, ch in enumerate(symbols):
        if ch == ".":
            if current_count == 0:
                # Nothing found yet
                continue

            if current_count != desired_count:
                # We have more # than we wanted, so it's already invalid
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


def recursive_eval(symbols: List[str], counts: List[int]) -> int:
    """
    Regular recursive evaluation for the `symbols` sequence.
    """

    # Cached value, we just return pre-computed result
    hash_name = "".join(symbols) + str(counts)
    if hash_name in cache.keys():
        return cache[hash_name]

    # We already filled all '?' symbols
    if all(value != "?" for value in symbols):
        return 1 if is_valid(symbols, counts) else 0

    # Too much or too few #s in the sequence
    if symbols.count("#") > sum(counts) or symbols.count("#") + symbols.count("?") < sum(counts):
        return 0

    # # Partial evaluation
    if not is_still_valid(symbols, counts):
        return 0

    index = symbols.index("?")

    # Find first #, and continue with subset
    found_occurrence = None
    for i, ch in enumerate(symbols):
        if ch == "#" and i < index:
            if all(s == "#" for s in symbols[i:i + counts[0]]) and symbols[i + counts[0]] == ".":
                found_occurrence = i
            break

    # Cutoff the first count from both `counts` and `symbols`
    if found_occurrence is not None:
        local_copy = symbols.copy()[found_occurrence + counts[0]:]
        index = local_copy.index("?")
        new_indices = counts[1:]
    else:
        local_copy = symbols.copy()
        new_indices = counts

    # Good matches in the subset
    local_copy[index] = "."
    good = recursive_eval(local_copy, new_indices)

    # Bad matches in the subset
    local_copy[index] = "#"
    bad = recursive_eval(local_copy, new_indices)

    cache[hash_name] = good + bad
    return good + bad


def unfold(symbols: str, counts: List[int], k: int) -> Tuple[str, List[int]]:
    flatten = []
    for inner_list in [counts] * k:
        flatten.extend(inner_list)
    return "?".join([symbols] * k), flatten


def evaluate(line: str) -> int:
    n = 5
    symbols, counts = line.strip().split(" ")
    counts = list(map(int, counts.split(",")))
    symbols, counts = unfold(symbols, counts, n)

    valid_combs = recursive_eval(list(symbols), counts)

    return valid_combs


if __name__ == '__main__':
    # Run pypy.exe 12p2.py for faster eval

    start = time.time()

    with open("input.txt", "r") as f:
        lines = f.readlines()

    with Pool(os.cpu_count()) as p:
        results = p.map(evaluate, lines)

    print(sum(results))
    print(time.time() - start)
