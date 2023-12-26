import itertools
import time
from typing import Tuple, Optional


def parse(line: str) -> Tuple[int, ...]:
    position, velocity = line.strip().split("@")
    px, py, pz = [int(x.strip()) for x in position.split(",")]
    vx, vy, vz = [int(x.strip()) for x in velocity.split(",")]
    return px, py, pz, vx, vy, vz


def evaluate(pair: Tuple) -> Optional[Tuple]:
    """
    Quick maffs solution
        y = a1x + b1
        y = a2x + b2
        a1x + b1 = a2x + b2
        (a1 - a2)x = b2 - b1
        x = (b2 - b1) / (a1 + a2)
        y = a1*x + b1
    """
    a1, b1 = _get_formula(pair[0])
    a2, b2 = _get_formula(pair[1])
    try:
        x = (b2 - b1) / (a1 - a2)
        y = a1 * x + b1
    except ZeroDivisionError:
        return None

    # Evaluate if the intersection is in the future
    def _is_future(_v: Tuple, _x: float, _y: float) -> bool:
        return abs(_v[0] - _x) > abs(_v[0] + _v[3] - _x) and abs(_v[1] - _y) > abs(_v[1] + _v[4] - _y)

    if _is_future(pair[0], x, y) and _is_future(pair[1], x, y):
        return x, y

    return None


def _get_formula(v: Tuple) -> Tuple:
    """
    Evaluates formula from two points, returning coefficients of y = ax = b.
    """
    c = 1
    x1, y1 = v[0], v[1]
    x2, y2 = v[0] + c * v[3], v[1] + c * v[4]
    a = (y2 - y1) / (x2 - x1)
    b = y1 - (a * x1)
    return a, b


if __name__ == '__main__':

    start = time.time()

    with open("input.txt", "r") as f:
        stones = [parse(line) for line in f]

    lower_bound = 200000000000000
    upper_bound = 400000000000000
    total = 0

    pairs = list(itertools.combinations(stones, r=2))

    for i, p in enumerate(pairs):
        result = evaluate(p)
        if result is not None and lower_bound <= result[0] <= upper_bound and lower_bound <= result[1] <= upper_bound:
            total += 1

    print(f"Total: {total}")
    print(f"Runtime: {time.time() - start}")
