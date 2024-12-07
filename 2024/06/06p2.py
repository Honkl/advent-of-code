import sys
import timeit
from copy import deepcopy
from multiprocessing import pool

sys.setrecursionlimit(10 ** 9)


class LoopException(Exception):
    pass


def rotate(direction: str) -> str:
    if direction == "^": return ">"
    if direction == ">": return "v"
    if direction == "v": return "<"
    if direction == "<": return "^"


def next_step(row: int, col: int, orientation: str) -> tuple[int, int]:
    if orientation == "^": return row - 1, col
    if orientation == ">": return row, col + 1
    if orientation == "v": return row + 1, col
    if orientation == "<": return row, col - 1


def follow(row: int, col: int, orientation: str, area: list[list[str]], visited: list[tuple[int, int, str]]) -> bool:
    # Guard is out of the map
    if row < 0 or row >= len(area) or col < 0 or col >= len(area[0]):
        return True

    # Already been in this configuration
    if (row, col, orientation) in visited:
        raise LoopException("Already visited!")

    # We stepped into the wall, return to previous position
    if area[row][col] == "#":
        return False

    visited.append((row, col, orientation))

    # We are ready to move
    success = False
    while not success:
        new_row, new_col = next_step(row, col, orientation)
        success = follow(new_row, new_col, orientation, area, visited)

        if not success:
            orientation = rotate(orientation)

    area[row][col] = "X"
    return True


def eval(arguments: tuple) -> bool:
    start_row, start_col, start_dir, wall_row, wall_col, grid = arguments

    # Create adjusted map
    map_copy = deepcopy(grid)
    map_copy[wall_row][wall_col] = "#"

    try:
        follow(start_row, start_col, start_dir, map_copy, visited=[])
        return False
    except LoopException:
        return True


def run() -> None:
    start = timeit.default_timer()

    with open("input.txt", "r") as f:
        game_map = []
        for line in f:
            game_map.append(list(line.strip()))

    # Get starting position
    start_row, start_col, start_dir = 0, 0, "^"
    for i in range(len(game_map)):
        for j in range(len(game_map[i])):
            if game_map[i][j] in ["<", ">", "v", "^"]:
                start_row, start_col = i, j
                start_dir = game_map[i][j]
                break

    # Get positions where normally would guard go
    testing_area = deepcopy(game_map)
    testing_area[start_row][start_col] = "X"
    follow(start_row, start_col, start_dir, testing_area, visited=[])

    game_map[start_row][start_col] = "."
    args = []
    for i in range(len(game_map)):
        for j in range(len(game_map[0])):
            if i == start_row and j == start_col:
                continue

            # Possible path-changing positions must be in original path
            if testing_area[i][j] == "X":
                args.append((start_row, start_col, start_dir, i, j, game_map))

            if len(args) >= 250:
                break
        if len(args) >= 250:
            break

    print(f"Total available placements: {len(args)}")

    with pool.Pool(16) as p:
        results = p.map(eval, args)

    # results = [eval(a) for a in args]

    print(f"Possible placements: {sum(results)}")
    print(f"Runtime: {timeit.default_timer() - start}s")


if __name__ == '__main__':
    run()
