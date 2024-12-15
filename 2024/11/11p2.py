import timeit

cache = {}


def expand(value: int, depth: int, max_depth: int) -> int:
    key = f"{value}-{depth}"

    if key in cache.keys():
        return cache[key]

    if depth == max_depth:
        return 1

    if value == 0:
        result = expand(1, depth + 1, max_depth)
    else:
        str_s = str(value)
        len_s = len(str(value))
        if len_s % 2 == 0:
            result = expand(
                int(str_s[:int(len_s / 2)]), depth + 1, max_depth
            ) + expand(
                int(str_s[int(len_s / 2):]), depth + 1, max_depth
            )

        else:
            result = expand(int(value) * 2024, depth + 1, max_depth)

    cache[key] = result
    return result


def expand_all(stones: list[int], max_depth: int) -> int:
    total = 0
    for s in stones:
        total += expand(value=s, depth=0, max_depth=max_depth)

    return total


def run() -> None:
    start = timeit.default_timer()

    with open("input.txt", "r") as f:
        stones = list(map(int, f.readline().strip().split(" ")))

    stones = expand_all(stones, max_depth=75)

    print(f"Total stones: {stones}")
    print(f"Runtime: {timeit.default_timer() - start}")


if __name__ == '__main__':
    run()
