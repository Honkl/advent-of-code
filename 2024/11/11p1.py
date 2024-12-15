import timeit


def step(stones: list[int]) -> list[int]:
    output = []
    for s in stones:
        if s == 0:
            output.append(1)
            continue

        str_s = str(s)
        len_s = len(str(s))
        if len_s % 2 == 0:
            output.append(int(str_s[:int(len_s / 2)]))
            output.append(int(str_s[int(len_s / 2):]))
            continue

        output.append(s * 2024)

    return output


def run() -> None:
    start = timeit.default_timer()

    with open("input.txt", "r") as f:
        stones = list(map(int, f.readline().strip().split(" ")))

    for i in range(25):
        stones = step(stones)

    print(f"Total stones: {len(stones)}")
    print(f"Runtime: {timeit.default_timer() - start}")


if __name__ == '__main__':
    run()
