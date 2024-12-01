if __name__ == '__main__':

    x, y = [], []
    with open("input.txt", "r") as f:
        for line in f:
            a, b = line.split("   ")
            x.append(int(a.strip()))
            y.append(int(b.strip()))

    total = 0
    for a, b in zip(sorted(x), sorted(y)):
        total += abs(a - b)

    print(total)
