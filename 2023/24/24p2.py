import time
from typing import Tuple, Optional, List

from sympy import Eq, solve, symbols


def parse(line: str) -> Tuple[int, ...]:
    position, velocity = line.strip().split("@")
    px, py, pz = [int(x.strip()) for x in position.split(",")]
    vx, vy, vz = [int(x.strip()) for x in velocity.split(",")]
    return px, py, pz, vx, vy, vz


def evaluate(points: List[Tuple]) -> Optional[Tuple]:
    """
    Not-so-quick maffs

    x   v1       r1
    y = v2 + a * r2
    z   v3       r3

    """
    equations = []
    velocity_variables = symbols("v0 v1 v2")
    variables = symbols(" ".join([f"a{i}" for i in range(len(points))]))
    for i in range(len(points) - 1):
        p1, p2 = points[i], points[i + 1]
        v1, v2 = variables[i], variables[i + 1]
        equations.append(Eq(p1[0] + v1 * (p1[3] - velocity_variables[0]), p2[0] + v2 * (p2[3] - velocity_variables[0])))
        equations.append(Eq(p1[1] + v1 * (p1[4] - velocity_variables[1]), p2[1] + v2 * (p2[4] - velocity_variables[1])))
        equations.append(Eq(p1[2] + v1 * (p1[5] - velocity_variables[2]), p2[2] + v2 * (p2[5] - velocity_variables[2])))

        # It turns out, that it is enough to find out solution for first N equations, and based off the design of the
        # task, it should work out (because there is an intersection). Otherwise, the number of equations included
        # into solver can be extended and in worst case scenario, all 897 equations will be solved
        if i >= 10:
            break

    solution = solve(equations, minimal=True)
    print(solution)

    # Set alpha to original formula to get intersection point
    if len(solution) > 0:
        p = points[0]  # taking first point, all should work
        s = solution[0]  # taking first solution
        a = s[variables[0]]
        x = p[0] + a * (p[3] - s[velocity_variables[0]])
        y = p[1] + a * (p[4] - s[velocity_variables[1]])
        z = p[2] + a * (p[5] - s[velocity_variables[2]])
        return x, y, z

    return None


if __name__ == '__main__':

    start = time.time()

    with open("input.txt", "r") as f:
        stones = [parse(line) for line in f]

    result = evaluate(stones)

    if result is not None:
        print(result[0] + result[1] + result[2])

    print(f"Runtime: {time.time() - start}")
