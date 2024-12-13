import timeit
import itertools


def is_valid(result: int, values: list[int]) -> bool:
    for solution in itertools.product(["+", "*", "||"], repeat=len(values) - 1):
        total_value = values[0]
        for operator, value in zip(solution, values[1:]):
            if operator == "+":
                total_value += value
            if operator == "*":
                total_value *= value
            if operator == "||":
                total_value = int(str(total_value) + str(value))

        if total_value == result:
            return True

    return False


if __name__ == '__main__':

    start = timeit.default_timer()

    with open("input.txt", "r") as f:
        equations = []
        for line in f:
            r, v = line.split(":")
            equations.append((
                int(r.strip()),
                list(map(int, v.strip().split(" ")))
            ))

    total = sum([r for r, v in equations if is_valid(r, v)])
    print(total)
    print(f"Runtime: {timeit.default_timer() - start}")
