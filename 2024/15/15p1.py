import timeit


def print_grid(grid: list[list[str]]) -> None:
    for i in range(len(grid)):
        print("".join(grid[i]))


def shift(grid: list[list[str]], i: int, j: int, new_i: int, new_j: int) -> tuple[int, int]:
    """Shifts robot and all objects in the path by single step."""
    if grid[new_i][new_j] == ".":
        grid[new_i][new_j] = "@"
        grid[i][j] = "."
        return new_i, new_j

    if grid[new_i][new_j] == "#":
        return i, j

    offset_i, offset_j = new_i - i, new_j - j

    objects_count = 0
    x, y = new_i, new_j
    while grid[x][y] == "O":
        objects_count += 1
        x, y = x + offset_i, y + offset_j

    if grid[x][y] == "#":
        return i, j

    if grid[x][y] == ".":
        grid[i][j] = "."
        grid[new_i][new_j] = "@"
        for k in range(1, objects_count + 1):
            grid[new_i + (k * offset_i)][new_j + (k * offset_j)] = "O"

        return new_i, new_j

    raise Exception("This should be unreachable")


def simulate(grid: list[list[str]], moves: list[str]) -> None:
    """Simulates the movement of the robot in the provided grid."""

    i, j = 0, 0
    stop = False
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "@":
                stop = True
                break
        if stop:
            break

    for move in moves:
        match move:
            case "<":
                i, j = shift(grid, i, j, i, j - 1)
            case ">":
                i, j = shift(grid, i, j, i, j + 1)
            case "^":
                i, j = shift(grid, i, j, i - 1, j)
            case "v":
                i, j = shift(grid, i, j, i + 1, j)


def run() -> None:
    grid = []
    moves = []
    with open("input.txt", "r") as f:

        grid_complete = False
        for line in f:

            if line.strip() == "":
                grid_complete = True
                continue

            if grid_complete:
                moves.extend(list(line.strip()))
            else:
                grid.append(list(line.strip()))

    simulate(grid, moves)
    print_grid(grid)

    gps = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "O":
                gps += 100 * i + j

    print(f"GPS: {gps}")


if __name__ == '__main__':
    start = timeit.default_timer()
    run()
    print(f"Runtime: {timeit.default_timer() - start}s")
