import timeit


def search(row: int, col: int, grid: list[list[int]]) -> int:
    stack = [(row, col)]

    pinnacles = []

    while len(stack) > 0:
        i, j = stack.pop()

        if grid[i][j] == 9:
            if (i, j) not in pinnacles:
                pinnacles.append((i, j))
            continue

        # Up
        if i - 1 >= 0 and grid[i][j] + 1 == grid[i - 1][j]:
            stack.append((i - 1, j))

        # Left
        if j - 1 >= 0 and grid[i][j] + 1 == grid[i][j - 1]:
            stack.append((i, j - 1))

        # Down
        if i + 1 < len(grid) and grid[i][j] + 1 == grid[i + 1][j]:
            stack.append((i + 1, j))

        # Right
        if j + 1 < len(grid[i]) and grid[i][j] + 1 == grid[i][j + 1]:
            stack.append((i, j + 1))

    return len(pinnacles)


def run() -> None:
    start = timeit.default_timer()

    grid = []
    with open("input.txt", "r") as f:
        for line in f:
            # grid.append(list(map(int, line.strip())))
            grid.append(list(map(int, [-1 if x == "." else x for x in line.strip()])))

    # Find all starting positions
    starts = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                starts.append((i, j))

    # Search from all starting positions
    total = sum(search(i, j, grid) for i, j in starts)

    print(f"Result: {total}")
    print(f"Runtime: {timeit.default_timer() - start}")


if __name__ == '__main__':
    run()
