def get_score(line: str) -> int:  # noqa
    values = line.split(":")[1]
    winning, current = values.split("|")

    winning = [int(v) for v in winning.strip().split(" ") if v != ""]
    current = [int(v) for v in current.strip().split(" ") if v != ""]

    match = [x for x in current if x in winning]
    return len(match)


if __name__ == '__main__':

    cards = {}
    with open("input.txt", "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            cards[i + 1] = get_score(line)

    counts = {c: 1 for c in cards.keys()}
    for card, score in cards.items():
        for i in range(score):
            counts[card + i + 1] += counts[card]

    print(sum(counts.values()))
