import os
import time
from copy import deepcopy
from multiprocessing import Pool
from typing import List, Tuple, Set


def settle(bricks: List[List[int]]) -> Tuple[List[List[int]], Set[int]]:
    change = True
    moved_bricks = set()
    while change:
        change = False
        for i in range(len(bricks)):
            can_move_down = True
            max_distance = None
            for j in range(len(bricks)):
                if i == j:
                    continue

                a = bricks[i]
                b = bricks[j]

                # Determine collision
                x_overlap = a[0] <= b[3] and b[0] <= a[3]
                y_overlap = a[1] <= b[4] and b[1] <= a[4]

                # Z distance to all lower/underlying bricks
                if max(b[2], b[5]) < min(a[2], a[5]):
                    z_distance = min(a[2], a[5]) - max(b[2], b[5])

                    # How much we can move
                    if (max_distance is None or z_distance < max_distance) and x_overlap and y_overlap:
                        max_distance = z_distance

                    if x_overlap and y_overlap and z_distance <= 1:
                        can_move_down = False
                        break

            # Move brick by N steps down
            if can_move_down and bricks[i][2] > 1 and bricks[i][5] > 1:

                if max_distance is None:
                    max_distance = 1
                else:
                    max_distance -= 1

                bricks[i][2] = max(1, bricks[i][2] - max_distance)
                bricks[i][5] = max(1, bricks[i][5] - max_distance)
                change = True
                moved_bricks.add(i)
                # print(f"Moving brick {i} - {bricks[i]} down by {max_distance}")
                break

    return bricks, moved_bricks


def can_disintegrate(params: Tuple) -> int:
    index, bricks_data = params
    new_copy = deepcopy(bricks_data)
    del new_copy[index]
    _, moved = settle(new_copy)
    return len(moved)


if __name__ == '__main__':
    # pypy 22p2.py
    start = time.time()

    with open("input.txt", "r") as f:
        data = [list(map(int, line.strip().replace("~", ",").split(","))) for line in f]

    data = sorted(data, key=lambda x: (x[2], x[5]))

    settled, _ = settle(data)

    args = [(i, settled) for i in range(len(settled))]

    # Determine disintegrate-able bricks
    with Pool(os.cpu_count()) as p:
        results = p.map(can_disintegrate, args)

    print(sum(results))
    print(f"Runtime: {time.time() - start}")
