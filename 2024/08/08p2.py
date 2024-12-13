import itertools
from copy import deepcopy


def mark_field(i: int, j: int, grid: list[list[str]]) -> None:
    if 0 <= i < len(grid) and 0 <= j < len(grid[i]):
        grid[i][j] = "#"


def mark_antinodes(
        ant_a: tuple[int, int],
        ant_b: tuple[int, int],
        grid: list[list[str]],
        antinodes_grid: list[list[str]]
) -> None:
    row_dist = ant_a[0] - ant_b[0]
    col_dist = ant_a[1] - ant_b[1]

    for i in range(0, len(grid)):
        new_row = ant_a[0] + (row_dist * i)
        new_col = ant_a[1] + (col_dist * i)
        mark_field(new_row, new_col, antinodes_grid)

        new_row = ant_a[0] - (row_dist * i)
        new_col = ant_a[1] - (col_dist * i)
        mark_field(new_row, new_col, antinodes_grid)


def run() -> None:
    with open("input.txt", "r") as f:
        grid = [list(line.strip()) for line in f]

    antinodes_grid = deepcopy(grid)

    antennas = {}
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            item = grid[i][j]
            if item != ".":
                if item not in antennas.keys():
                    antennas[item] = []
                antennas[item].append((i, j))

    for positions in antennas.values():
        for pair in list(itertools.combinations(positions, 2)):
            mark_antinodes(pair[0], pair[1], grid, antinodes_grid)

    total = sum([row.count("#") for row in antinodes_grid])
    print(total)


if __name__ == '__main__':
    run()
