if __name__ == '__main__':

    x, y = [], []
    with open("input.txt", "r") as f:
        for line in f:
            a, b = line.split("   ")
            x.append(int(a.strip()))
            y.append(int(b.strip()))

    score = 0
    for a in x:
        score += a * y.count(a)

    print(score)
