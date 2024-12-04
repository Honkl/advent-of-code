def is_xmas(row: int, col: int) -> bool:
    conditions = [
        [
            grid[row][col] == "A",
            grid[row - 1][col - 1] == "M",
            grid[row - 1][col + 1] == "S",
            grid[row + 1][col - 1] == "M",
            grid[row + 1][col + 1] == "S",
        ],
        [
            grid[row][col] == "A",
            grid[row - 1][col - 1] == "S",
            grid[row - 1][col + 1] == "S",
            grid[row + 1][col - 1] == "M",
            grid[row + 1][col + 1] == "M",
        ],
        [
            grid[row][col] == "A",
            grid[row - 1][col - 1] == "S",
            grid[row - 1][col + 1] == "M",
            grid[row + 1][col - 1] == "S",
            grid[row + 1][col + 1] == "M",
        ],
        [
            grid[row][col] == "A",
            grid[row - 1][col - 1] == "M",
            grid[row - 1][col + 1] == "M",
            grid[row + 1][col - 1] == "S",
            grid[row + 1][col + 1] == "S",
        ]
    ]
    return any(all(sub_conditions) for sub_conditions in conditions)


if __name__ == '__main__':

    with open("input.txt", "r") as f:
        grid = []
        for line in f:
            grid.append(list(line.strip()))

    total = 0

    for row in range(1, len(grid) - 1):
        for col in range(1, len(grid) - 1):
            if is_xmas(row, col):
                total += 1

    print(total)
