class N:
    value: int

    def __init__(self, value) -> None:
        self.value = value

    def __lt__(self, other) -> bool:
        for r in rules:
            if r[0] == self.value and r[1] == other.value:
                return True
        return False

    def __repr__(self) -> str:
        return str(self.value)


def is_correct(update: list[int]) -> bool:
    printed = []
    for n in update:

        for r in rules:
            # Skip irrelevant rules (update must contain both numbers from the rule)
            if r[0] not in update or r[1] not in update:
                continue

            if n == r[1] and r[0] not in printed:
                return False

        printed.append(n)

    return True


def get_middle_number(update: list[N]) -> int:
    assert len(update) % 2 == 1
    return update[int(len(update) / 2)].value


if __name__ == '__main__':

    rules, updates = [], []

    with open("input.txt", "r") as f:
        for line in f:
            if "|" in line:
                rules.append(list(map(int, line.strip().split("|"))))
            elif "," in line:
                updates.append(list(map(int, line.strip().split(","))))

    incorrect_updates = [u for u in updates if not is_correct(u)]
    print(incorrect_updates)
    fixed_updates = [sorted([N(n) for n in u]) for u in incorrect_updates]
    print(fixed_updates)
    total = sum(get_middle_number(u) for u in fixed_updates)

    print(total)
