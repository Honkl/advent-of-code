import time
from copy import deepcopy

if __name__ == '__main__':
    start = time.time()

    field = []
    start_i, start_j = 0, 0
    with open("input.txt", "r") as f:
        for i, line in enumerate(f):
            if "S" in line:
                start_i = i
                start_j = line.index("S")
                line = line.replace("S", ".")
            field.append(list(line.strip()))

    print(f"Starting position: {start_i, start_j}")

    visited = deepcopy(field)
    for i in range(len(field)):
        for j in range(len(field[i])):
            visited[i][j] = []

    queue = [(start_i, start_j, 0)]
    target = 64
    steps = 0
    last_print = 0
    while len(queue) > 0:
        i, j, steps = queue.pop(0)
        if steps > target:
            continue

        if steps in visited[i][j]:
            continue

        visited[i][j].append(steps)

        if i > 0 and field[i - 1][j] == ".":
            queue.append((i - 1, j, steps + 1))
        if j > 0 and field[i][j - 1] == ".":
            queue.append((i, j - 1, steps + 1))
        if i < len(field) - 1 and field[i + 1][j] == ".":
            queue.append((i + 1, j, steps + 1))
        if j < len(field[i]) - 1 and field[i][j + 1] == ".":
            queue.append((i, j + 1, steps + 1))

        if steps > last_print:
            last_print = steps

    total = sum([sum(1 for x in visited[i] if target in x) for i in range(len(visited))])
    print(total)
    print(time.time() - start)
