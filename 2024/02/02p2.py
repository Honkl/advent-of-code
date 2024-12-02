def is_safe(r: list[int]) -> bool:
    safe = True
    inc, dec = False, False

    for i in range(len(r) - 1):
        if abs(r[i] - r[i + 1]) < 1 or abs(r[i] - r[i + 1]) > 3:
            safe = False
            break
        if r[i] < r[i + 1]:
            inc = True
        else:
            dec = True

    return safe and (inc != dec)


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        reports = [list(map(int, line.split(" "))) for line in f]

    total = 0
    for rep in reports:
        if is_safe(rep):
            total += 1
        else:
            for i in range(len(rep)):
                if is_safe(rep[:i] + rep[i + 1:]):
                    total += 1
                    break

    print(total)
