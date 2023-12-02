def extract(value: str) -> int:
    output = None

    for ch in value:
        if ch.isnumeric():
            output = ch
            break

    if output is None:
        raise Exception(f"Missing number in value: {value}")

    for ch in "".join(reversed(value)):
        if ch.isnumeric():
            output += ch
            break

    return int(output)


if __name__ == '__main__':
    total = 0
    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            total += extract(line.strip())

    print(total)
