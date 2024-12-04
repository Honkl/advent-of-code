def is_xmas(coordinates: list[tuple[int, int]]) -> bool:
    word = "".join(
        grid[r][c] for r, c in coordinates if 0 <= r < height and 0 <= c < width
    )
    return word == target


def find_occurrences(row: int, col: int) -> int:
    findings = [
        is_xmas([(row, col + i) for i in range(size)]),  # right
        is_xmas([(row + i, col + i) for i in range(size)]),  # right-bottom
        is_xmas([(row + i, col) for i in range(size)]),  # bottom
        is_xmas([(row + i, col - i) for i in range(size)]),  # left-bottom
        is_xmas([(row, col - i) for i in range(size)]),  # left
        is_xmas([(row - i, col - i) for i in range(size)]),  # left-up
        is_xmas([(row - i, col) for i in range(size)]),  # up
        is_xmas([(row - i, col + i) for i in range(size)]),  # right-up
    ]
    return sum(findings)


if __name__ == '__main__':

    with open("input.txt", "r") as f:
        grid = []
        for line in f:
            grid.append(list(line.strip()))

    target = "XMAS"
    size = len(target)
    height = len(grid)
    width = len(grid[0])

    total = 0

    for row in range(len(grid)):
        for col in range(len(grid)):
            total += find_occurrences(row, col)

    print(total)
