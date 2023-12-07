def any_eq(counts: dict, x: int) -> bool:
    return any(x == y for y in counts.values())


class Card:
    value: str
    bid: int
    kind: int

    def __init__(self, value: str, bid: int) -> None:
        self.value = value
        self.bid = bid

        # Evaluate card's kind
        counts = {}
        for ch in value:
            if ch not in counts.keys():
                counts[ch] = 0
            counts[ch] += 1

        if len(counts.keys()) == 1:
            kind = 7
        elif len(counts.keys()) == 2 and any_eq(counts, 4):
            kind = 6
        elif len(counts.keys()) == 2 and any_eq(counts, 3) and any_eq(counts, 2):
            kind = 5
        elif len(counts.keys()) == 3 and any_eq(counts, 3) and any_eq(counts, 1):
            kind = 4
        elif len(counts.keys()) == 3 and any_eq(counts, 2) and any_eq(counts, 1):
            kind = 3
        elif len(counts.keys()) == 4:
            kind = 2
        elif len(counts.keys()) == 5:
            kind = 1
        else:
            raise ValueError(value)

        self.kind = kind

    def __repr__(self) -> str:
        return f"Card({self.value}, {self.bid}, {self.kind})"

    def __eq__(self, other: "Card") -> bool:
        return False

    def __lt__(self, other: "Card") -> bool:
        if self.kind < other.kind:
            return True
        if self.kind > other.kind:
            return False

        symbols = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
        for i in range(len(self.value)):
            j = symbols.index(self.value[i])
            k = symbols.index(other.value[i])
            if j == k:
                continue
            if j < k:
                return False
            return True


if __name__ == '__main__':

    cards = []
    with open("input.txt", "r", encoding="utf-8") as f:
        for line in f:
            v, b = line.split(" ")
            cards.append(Card(v.strip(), int(b.strip())))

    print(cards)
    cards = list(sorted(cards))
    print(cards)

    total = 0
    for i, c in enumerate(cards):
        total += c.bid * (i + 1)

    print(total)
