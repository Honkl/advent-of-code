import sys
import time
from enum import Enum
from typing import Tuple, List

sys.setrecursionlimit(10 ** 6)


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    @staticmethod
    def opposite(other: "Direction") -> "Direction":
        return {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }[other]


visited = {}


def search(i: int, j: int, d: Direction, steps: int, heat_loss: int, min_heat_loss: int) -> int | List[Tuple]:
    key = f"{i}-{j}-{d}-{steps}"
    if key in visited.keys() and visited[key] <= heat_loss:
        return max_loss
    visited[key] = heat_loss

    # Final target node
    if (i, j) == target:
        return heat_loss

    # Wrong path, we have already better one
    if min_heat_loss is not None and min_heat_loss <= heat_loss:
        return heat_loss

    new_args = []
    for next_d in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:

        # We have reached max steps in this direction, skipping
        if next_d == d and steps == max_steps:
            continue

        # Top or bottom boundaries of the map
        if (next_d == Direction.UP and i == 0) or (next_d == Direction.DOWN and i == len(data) - 1):
            continue

        # Left or right boundaries of the map
        if (next_d == Direction.LEFT and j == 0) or (next_d == Direction.RIGHT and j == len(data[i]) - 1):
            continue

        # Can't go in opposite direction
        if next_d == Direction.opposite(d):
            continue

        next_steps = 1 if next_d != d else steps + 1
        next_i = i if next_d not in [Direction.UP, Direction.DOWN] else i + 1 if next_d == Direction.DOWN else i - 1
        next_j = j if next_d not in [Direction.LEFT, Direction.RIGHT] else j + 1 if next_d == Direction.RIGHT else j - 1
        new_args.append((next_i, next_j, next_d, next_steps, heat_loss + data[next_i][next_j]))

    return new_args


if __name__ == '__main__':
    start = time.time()

    with open("input.txt", "r") as f:
        data = [list(map(int, line.strip())) for line in f]

    target = (len(data) - 1, len(data[-1]) - 1)
    max_steps = 3
    max_loss = sum(sum(x) for x in data)

    queue = [
        (0, 0, Direction.RIGHT, 0, 0),
    ]
    min_loss = None
    while len(queue) > 0:
        args = queue.pop()

        result = search(*args, min_loss)

        if isinstance(result, int):
            if min_loss is None or min_loss > result:
                min_loss = result
                print(min_loss, len(queue))

        else:
            queue.extend(result)

    # search_down = search(i=0, j=0, d=Direction.DOWN, steps=0, heat_loss=0)
    # (0, 0, Direction.DOWN, 0, 0)

    print()
    print(min_loss)
    print(time.time() - start)
