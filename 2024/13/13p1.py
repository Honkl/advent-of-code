import timeit
from typing import Optional

from sympy import Eq, solve, symbols
from sympy.core.numbers import Integer


def parse_data() -> list[dict[str, tuple[int, int]]]:
    machines = []
    machine = {}

    with open("input.txt", "r") as f:
        for line in f:

            if line.strip() == "":
                machines.append(machine)
                machine = {}

            elif "A" in line or "B" in line:
                button = "A" if "A" in line else "B"
                x, y = line.split(":")[1].strip().split(",")
                machine[button] = (
                    int(x.split("+")[1].strip()),
                    int(y.split("+")[1].strip()),
                )

            else:
                x, y = line.split(":")[1].strip().split(",")
                machine["Prize"] = (
                    int(x.strip().split("=")[1].strip()),
                    int(y.strip().split("=")[1].strip()),
                )

    machines.append(machine)
    return machines


def evaluate(machine: dict[str, tuple[int, int]]) -> Optional[tuple[int, int]]:
    a, b = symbols("a b")
    equations = [
        Eq(machine["Prize"][i], machine["A"][i] * a + machine["B"][i] * b) for i in range(2)
    ]
    solution = solve(equations)

    if isinstance(solution[a], Integer) and isinstance(solution[b], Integer):
        return int(solution[a]), int(solution[b])

    return None


def run() -> None:
    machines = parse_data()

    total = 0
    for m in machines:
        result = evaluate(m)
        if result:
            total += (3 * result[0]) + (1 * result[1])

    print(f"Total: {total}")


if __name__ == '__main__':
    start = timeit.default_timer()
    run()
    print(f"Runtime: {timeit.default_timer() - start}s")
