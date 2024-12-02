if __name__ == '__main__':
    with open("input.txt", "r") as f:
        reports = [list(map(int, line.split(" "))) for line in f]

    total = 0
    for r in reports:
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

        total += 0 if (inc and dec) or (not safe) else 1

    print(total)
