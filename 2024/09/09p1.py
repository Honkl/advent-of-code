import timeit


def expand(line: str) -> list[str]:
    result = []
    index = 0
    is_file = True
    while len(line) > 0:
        item = line[0]

        for _ in range(int(item)):
            if is_file:
                result.append(str(index))
            else:
                result.append(".")

        if is_file:
            index += 1

        is_file = not is_file
        line = line[1:]

    return result


def shuffle(line: list[str]) -> list[str]:
    i = 0
    j = len(line) - 1

    result = []
    number_count = sum(1 for value in line if value != ".")

    while len(result) < number_count:
        if line[i] == ".":
            while line[j] == ".":
                j -= 1
            result.append(line[j])
            j -= 1
        else:
            result.append(line[i])
        i += 1

    return result


def run() -> None:
    start = timeit.default_timer()

    with open("input.txt", "r") as f:
        line = f.readline().strip()

    exp = expand(line)
    shuffled = shuffle(exp)

    total = sum(i * int(value) for i, value in enumerate(shuffled))
    print(f"Result: {total}")
    print(f"Runtime: {timeit.default_timer() - start}")


if __name__ == '__main__':
    run()
