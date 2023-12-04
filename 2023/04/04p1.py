def get_score(line: str) -> int:  # noqa
    values = line.split(":")[1]
    winning, current = values.split("|")

    winning = [int(v) for v in winning.strip().split(" ") if v != ""]
    current = [int(v) for v in current.strip().split(" ") if v != ""]

    match = [x for x in current if x in winning]
    if len(match) == 0:
        return 0
    return 2 ** max((len(match) - 1), 0)


if __name__ == '__main__':
    total = 0
    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            total += get_score(line)
    print(total)
