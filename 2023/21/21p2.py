import time
from typing import List

from sympy import Eq, solve, symbols


def can_go(i: int, j: int, field: List) -> bool:  # noqa
    new_i, new_j = i, j

    if i < 0 or i >= len(field):
        new_i = i % len(field)
    if j < 0 or j >= len(field[i % len(field)]):
        new_j = j % len(field[i % len(field)])

    return field[new_i][new_j] == "."


def score(visited: List, at_step: int) -> int:
    total = 0
    for k, v in visited.items():
        if v > at_step:
            continue
        if v % 2 == at_step % 2:
            total += 1
    return total


if __name__ == '__main__':
    start = time.time()

    field = []
    start_i, start_j = 0, 0
    with open("input.txt", "r") as f:
        for i, line in enumerate(f):
            if "S" in line:
                start_i = i
                start_j = line.index("S")
                line = line.replace("S", ".")
            field.append(list(line.strip()))

    print(f"Starting position: {start_i, start_j}")

    visited = {}
    queue = [(start_i, start_j, 0)]
    target = 500  # Set target up to any value that is needed
    steps = 0
    last_print = 0
    while len(queue) > 0:
        i, j, steps = queue.pop(0)

        if steps > target:
            continue

        key = f"{i}-{j}"
        if key in visited.keys():
            continue

        visited[key] = steps

        if can_go(i - 1, j, field):
            queue.append((i - 1, j, steps + 1))
        if can_go(i + 1, j, field):
            queue.append((i + 1, j, steps + 1))
        if can_go(i, j - 1, field):
            queue.append((i, j - 1, steps + 1))
        if can_go(i, j + 1, field):
            queue.append((i, j + 1, steps + 1))

        if steps > last_print:
            last_print = steps

    width = len(field[0])
    print(width)

    scores = {}

    # Confession: these numbers had to be searched for, it's actually f(x) = ax2 + bx + c and to determine values,
    # we need n+1 points for polynom of order n. Target value is divisible by 65 and it's on the curve.
    # This was kinda bs, would not be able to come up with this, probably...
    for s in [65, 65 + width, 65 + 2 * width]:
        scores[s] = score(visited, s)
        print(f"Steps: {s}, Score: {scores[s]}")

    print(scores.items())

    a, b, c = symbols("a b c")
    equations = [
        Eq(y, a * x ** 2 + b * x + c) for x, y in scores.items()
    ]

    solution = solve(equations)
    print(solution)

    # Reconstruct formula
    for t in [6, 10, 50, 100, 500, 1000, 5000, 26501365]:
        y = solution[a] * t ** 2 + solution[b] * t + solution[c]
        print(f"Target={t} ==> {float(y)}")

    print(f"Runtime: {time.time() - start}")
