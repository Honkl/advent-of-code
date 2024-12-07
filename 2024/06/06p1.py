import sys
import timeit

sys.setrecursionlimit(10 ** 6)


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


def follow(row: int, col: int, orientation: str) -> bool:
    # Guard is out of the map
    if row < 0 or row >= len(area) or col < 0 or col >= len(area[0]):
        return True

    # We stepped into the wall, return to previous position
    if area[row][col] == "#":
        return False

    # We are ready to move
    success = False
    while not success:
        new_row, new_col = next_step(row, col, orientation)
        success = follow(new_row, new_col, orientation)

        if not success:
            orientation = rotate(orientation)

    area[row][col] = "X"
    return True


def print_map() -> None:
    for row in area:
        print("".join(row))


if __name__ == '__main__':

    start = timeit.default_timer()

    with open("input.txt", "r") as f:
        area = []
        for line in f:
            area.append(list(line.strip()))

    # Get starting position
    start_row, start_col, start_dir = 0, 0, "^"
    for i in range(len(area)):
        for j in range(len(area[i])):
            if area[i][j] in ["<", ">", "v", "^"]:
                start_row, start_col = i, j
                start_dir = area[i][j]
                break

    area[start_row][start_col] = "X"
    print(f"Starting position: [{start_row},{start_col}]")

    follow(start_row, start_col, start_dir)

    total = sum(len([p for p in row if p == "X"]) for row in area)

    print(f"Total visited positions: {total}")
    print(f"Runtime: {timeit.default_timer() - start}s")
