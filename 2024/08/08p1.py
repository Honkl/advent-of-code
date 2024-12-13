def is_antinode(row: int, col: int, grid: list[list[str]]) -> bool:
    for i in range(len(grid)):
        for j in range(len(grid[i])):

            if i == row and j == col:
                continue

            item = grid[i][j]
            if item != ".":

                row_dist = i - row
                col_dist = j - col

                double_row_position = row + (2 * row_dist)
                double_col_position = col + (2 * col_dist)

                if 0 <= double_row_position < len(grid) and 0 <= double_col_position < len(grid[row]):
                    if grid[double_row_position][double_col_position] == item:
                        return True

    return False


def run() -> None:
    with open("input.txt", "r") as f:
        grid = [list(line.strip()) for line in f]

    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if is_antinode(i, j, grid):
                total += 1

    print(total)


if __name__ == '__main__':
    run()
