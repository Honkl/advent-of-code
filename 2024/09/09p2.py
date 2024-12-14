import timeit


def expand(line: str) -> list[list[str]]:
    result = []
    index = 0
    is_file = True
    while len(line) > 0:
        item = line[0]

        inner_list = []
        for _ in range(int(item)):
            inner_list.append(str(index) if is_file else ".")

        if len(inner_list) > 0:
            result.append(inner_list)

        if is_file:
            index += 1

        is_file = not is_file
        line = line[1:]

    return result


def shuffle(line: list[list[str]]) -> list[list[str]]:
    i = 0
    exit_iteration = False

    while i < len(line):
        j = len(line) - 1

        if line[i][0] == ".":
            while len(line[j]) > len(line[i]) or line[j][0] == ".":
                j -= 1
                if j <= i:
                    i += 1
                    exit_iteration = True
                    break

            if exit_iteration:
                exit_iteration = False
                continue

            numbers = line[j]
            spaces = line[i]

            line[i] = numbers
            line[j] = spaces

            if len(numbers) < len(spaces):
                line.insert(i + 1, ["."] * (len(spaces) - len(numbers)))
                line[j + 1] = line[j + 1][:len(numbers)]
            else:
                i += 1

        else:
            i += 1

    return line


def run() -> None:
    start = timeit.default_timer()

    with open("input.txt", "r") as f:
        line = f.readline().strip()

    exp = expand(line)
    shuffled = shuffle(exp)

    flatten = [value for inner in shuffled for value in inner]
    total = sum(i * int(value) for i, value in enumerate(flatten) if value != ".")
    print(f"Result: {total}")
    print(f"Runtime: {timeit.default_timer() - start}")


if __name__ == '__main__':
    run()
