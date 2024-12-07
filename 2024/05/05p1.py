def is_correct(update: list[int], rules: list[list[int]]) -> bool:  # noqa

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


def get_middle_number(update: list[int]) -> int:
    assert len(update) % 2 == 1
    return update[int(len(update) / 2)]


if __name__ == '__main__':

    rules, updates = [], []

    with open("input.txt", "r") as f:
        for line in f:
            if "|" in line:
                rules.append(list(map(int, line.strip().split("|"))))
            elif "," in line:
                updates.append(list(map(int, line.strip().split(","))))

    correct_updates = [u for u in updates if is_correct(u, rules)]
    total = sum(get_middle_number(u) for u in correct_updates)

    print(total)
