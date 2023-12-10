import sys
from enum import Enum
from typing import Tuple, List

sys.setrecursionlimit(10 ** 6)

with open("input.txt", "r") as f:
    field = [line.strip() for line in f]

sides = [list(row) for row in field]


def print_sides() -> None:
    print()
    for row in sides:
        print(row)
    print()


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    @staticmethod
    def all_directions() -> List["Direction"]:
        return [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]


valid_entry_points = {
    "|": [Direction.UP, Direction.DOWN],
    "-": [Direction.LEFT, Direction.RIGHT],
    "L": [Direction.DOWN, Direction.LEFT],
    "J": [Direction.DOWN, Direction.RIGHT],
    "7": [Direction.UP, Direction.RIGHT],
    "F": [Direction.UP, Direction.LEFT],
    ".": [],
}

outbound_directions = {
    "|": {Direction.UP: Direction.UP, Direction.DOWN: Direction.DOWN},
    "-": {Direction.LEFT: Direction.LEFT, Direction.RIGHT: Direction.RIGHT},
    "L": {Direction.DOWN: Direction.RIGHT, Direction.LEFT: Direction.UP},
    "J": {Direction.DOWN: Direction.LEFT, Direction.RIGHT: Direction.UP},
    "7": {Direction.UP: Direction.LEFT, Direction.RIGHT: Direction.DOWN},
    "F": {Direction.UP: Direction.RIGHT, Direction.LEFT: Direction.DOWN},
    ".": [],
}


def is_valid(symbol: str, direction: Direction) -> bool:
    return direction in valid_entry_points[symbol]


def follow(
        i: int,
        j: int,
        start_i: int,
        start_j: int,
        direction: Direction,
        depth: int,
        path: List[Tuple[int, int, Direction]]
) -> Tuple[bool, int, List[Tuple[int, int, Direction]]]:
    # Back to the original starting location
    if i == start_i and j == start_j:
        return True, depth, path

    try:
        symbol = field[i][j]
    except:  # noqa
        return False, depth, []

    if not is_valid(symbol, direction):
        return False, depth, []

    next_direction = outbound_directions[symbol][direction]
    path.append((i, j, next_direction))
    if next_direction == Direction.UP:
        return follow(i - 1, j, start_i, start_j, next_direction, depth + 1, path)
    if next_direction == Direction.DOWN:
        return follow(i + 1, j, start_i, start_j, next_direction, depth + 1, path)
    if next_direction == Direction.LEFT:
        return follow(i, j - 1, start_i, start_j, next_direction, depth + 1, path)
    if next_direction == Direction.RIGHT:
        return follow(i, j + 1, start_i, start_j, next_direction, depth + 1, path)


def get_start() -> Tuple[int, int]:
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == "S":
                return i, j


def is_on_the_path(i: int, j: int, path: List[Tuple[int, int, Direction]]):
    for m, n, _ in path:
        if i == m and j == n:
            return True
    return False


def assign_sides(path: List[Tuple[int, int, Direction]]) -> Tuple[int, int]:
    for i, j, direction in path:
        if i == 3 and j == 15:
            print_sides()
        symbol = field[i][j]

        # Side is not assigned if it was already assigned before, or it is on the path for each symbol

        if symbol == "|":
            if j - 1 >= 0:
                next_symbol = sides[i][j - 1]
                if next_symbol not in ["X", "Y"] and not is_on_the_path(i, j - 1, path):
                    sides[i][j - 1] = "X" if direction == Direction.DOWN else "Y"

            if j + 1 < len(field[0]):
                next_symbol = sides[i][j + 1]
                if next_symbol not in ["X", "Y"] and not is_on_the_path(i, j + 1, path):
                    sides[i][j + 1] = "Y" if direction == Direction.DOWN else "X"

        if symbol == "-":
            if i - 1 >= 0:
                next_symbol = sides[i - 1][j]
                if next_symbol not in ["X", "Y"] and not is_on_the_path(i - 1, j, path):
                    sides[i - 1][j] = "X" if direction == Direction.LEFT else "Y"

            if i + 1 < len(field):
                next_symbol = sides[i + 1][j]
                if next_symbol not in ["X", "Y"] and not is_on_the_path(i + 1, j, path):
                    sides[i + 1][j] = "Y" if direction == Direction.LEFT else "X"

        if symbol == "L":
            if j - 1 >= 0:
                next_symbol = sides[i][j - 1]
                if next_symbol not in ["X", "Y"] and not is_on_the_path(i, j - 1, path):
                    sides[i][j - 1] = "X" if direction == Direction.RIGHT else "Y"

            if i + 1 < len(field):
                next_symbol = sides[i + 1][j]
                if next_symbol not in ["X", "Y"] and not is_on_the_path(i + 1, j, path):
                    sides[i + 1][j] = "X" if direction == Direction.RIGHT else "Y"

        if symbol == "J":
            if j + 1 < len(field[0]):
                next_symbol = sides[i][j + 1]
                if next_symbol not in ["X", "Y"] and not is_on_the_path(i, j + 1, path):
                    sides[i][j + 1] = "X" if direction == Direction.UP else "Y"

            if i + 1 < len(field):
                next_symbol = sides[i + 1][j]
                if next_symbol not in ["X", "Y"] and not is_on_the_path(i + 1, j, path):
                    sides[i + 1][j] = "X" if direction == Direction.UP else "Y"

        if symbol == "F":
            if i - 1 >= 0:
                next_symbol = sides[i - 1][j]
                if next_symbol not in ["X", "Y"] and not is_on_the_path(i - 1, j, path):
                    sides[i - 1][j] = "Y" if direction == Direction.RIGHT else "X"

            if j - 1 >= 0:
                next_symbol = sides[i][j - 1]
                if next_symbol not in ["X", "Y"] and not is_on_the_path(i, j - 1, path):
                    sides[i][j - 1] = "Y" if direction == Direction.RIGHT else "X"

        if symbol == "7":
            if i - 1 >= 0:
                next_symbol = sides[i - 1][j]
                if next_symbol not in ["X", "Y"] and not is_on_the_path(i - 1, j, path):
                    sides[i - 1][j] = "Y" if direction == Direction.DOWN else "X"

            if j + 1 < len(field[0]):
                next_symbol = sides[i][j + 1]
                if next_symbol not in ["X", "Y"] and not is_on_the_path(i, j + 1, path):
                    sides[i][j + 1] = "Y" if direction == Direction.DOWN else "X"

    change = True
    while change:
        change = False
        for i in range(len(sides)):
            for j in range(len(sides[i])):
                if is_on_the_path(i, j, path):
                    continue

                # Assign same side as neighbour
                if sides[i][j] not in ["X", "Y"]:
                    for m, n in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                        try:
                            symbol = sides[m][n]
                        except:  # noqa
                            continue
                        if symbol in ["X", "Y"]:
                            sides[i][j] = sides[m][n]
                            change = True

    x, y = 0, 0
    for i in range(len(sides)):
        for j in range(len(sides[i])):
            if sides[i][j] == "X":
                x += 1
            if sides[i][j] == "Y":
                y += 1

    return x, y


if __name__ == '__main__':
    ii, jj = get_start()
    print(f"Starting location={ii}:{jj}")

    path_ = []
    for dr in Direction.all_directions():
        next_ii, next_jj = ii, jj
        if dr == Direction.UP:
            next_ii = ii - 1
        if dr == Direction.DOWN:
            next_ii = ii + 1
        if dr == Direction.LEFT:
            next_jj = next_jj - 1
        if dr == Direction.RIGHT:
            next_jj = jj + 1

        loop, depth_, path_ = follow(next_ii, next_jj, ii, jj, dr, 1, [(ii, jj, dr)])
        print(f"Start direction={dr}, Loop={loop}, Length={depth_ / 2}")

        if loop:
            break

    counts_x, counts_y = assign_sides(path_)
    print_sides()
    print(counts_x, counts_y)
