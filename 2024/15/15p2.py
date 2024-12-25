# Ugly solution, can improve a lot
import timeit


def print_grid(grid: list[list[str]]) -> None:
    for i in range(len(grid)):
        print("".join(grid[i]))


def can_shift(grid: list[list[str]], i: int, j: int, new_i: int, new_j: int) -> bool:
    if grid[new_i][new_j] == ".":
        return True

    offset_i, offset_j = new_i - i, new_j - j
    if grid[new_i][new_j] == "[":
        return all([
            can_shift(grid, new_i, new_j, new_i + offset_i, new_j + offset_j),
            can_shift(grid, new_i, new_j + 1, new_i + offset_i, new_j + offset_j + 1),
        ])

    if grid[new_i][new_j] == "]":
        return all([
            can_shift(grid, new_i, new_j, new_i + offset_i, new_j + offset_j),
            can_shift(grid, new_i, new_j - 1, new_i + offset_i, new_j + offset_j - 1),
        ])


def shift(grid: list[list[str]], i: int, j: int, new_i: int, new_j: int, value: str) -> tuple[int, int]:
    """Shifts robot and all objects in the path by single step."""

    if grid[new_i][new_j] == ".":
        grid[new_i][new_j] = grid[i][j]
        grid[i][j] = value
        return new_i, new_j

    if grid[new_i][new_j] == "#":
        return i, j

    offset_i, offset_j = new_i - i, new_j - j

    # Only horizontal shift, no complicated situations included
    if offset_i == 0:
        objects = []
        x, y = new_i, new_j
        while grid[x][y] in ["[", "]"]:
            objects.append(grid[x][y])
            x, y = x + offset_i, y + offset_j

        if grid[x][y] == "#":
            return i, j

        objects = list(reversed(objects))

        if grid[x][y] == ".":
            grid[new_i][new_j] = grid[i][j]
            grid[i][j] = value
            for k in range(1, len(objects) + 1):
                grid[new_i + (k * offset_i)][new_j + (k * offset_j)] = objects.pop()

            return new_i, new_j

    # Vertical shift, complicated situation, need to check stairs-like arrangement
    else:
        if not can_shift(grid, i, j, new_i, new_j):
            return i, j

        current_value = grid[i][j]
        next_value = grid[new_i][new_j]

        if next_value == "[":
            shift(grid, new_i, new_j, new_i + offset_i, new_j + offset_j, next_value)
            shift(grid, new_i, new_j + 1, new_i + offset_i, new_j + offset_j + 1, ".")
        if next_value == "]":
            shift(grid, new_i, new_j, new_i + offset_i, new_j + offset_j, next_value)
            shift(grid, new_i, new_j - 1, new_i + offset_i, new_j + offset_j - 1, ".")
        if next_value == ".":
            shift(grid, new_i, new_j, new_i + offset_i, new_j + offset_j, next_value)

        grid[i][j] = value
        grid[new_i][new_j] = current_value

        return new_i, new_j


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
                i, j = shift(grid, i, j, i, j - 1, ".")
            case ">":
                i, j = shift(grid, i, j, i, j + 1, ".")
            case "^":
                i, j = shift(grid, i, j, i - 1, j, ".")
            case "v":
                i, j = shift(grid, i, j, i + 1, j, ".")


def expand(grid: list[list[str]]) -> list[list[str]]:
    new_grid = []
    for i in range(len(grid)):
        new_row = []
        for j in range(len(grid[i])):
            match grid[i][j]:
                case "#":
                    new_row.extend(["#", "#"])
                case "O":
                    new_row.extend(["[", "]"])
                case ".":
                    new_row.extend([".", "."])
                case "@":
                    new_row.extend(["@", "."])
        new_grid.append(new_row)
    return new_grid


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

    grid = expand(grid)
    simulate(grid, moves)

    gps = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "[":
                gps += 100 * i + j

    print(f"GPS: {gps}")


if __name__ == '__main__':
    start = timeit.default_timer()
    run()
    print(f"Runtime: {timeit.default_timer() - start}s")
