if __name__ == '__main__':

    vertices = []
    x, y = 0, 0
    circuit = 0
    with open("input.txt", "r") as f:
        for line in f:
            d, v, _ = line.strip().split(" ")
            v = int(v)
            circuit += v

            if d == "R":
                x += v
            if d == "L":
                x -= v
            if d == "U":
                y += v
            if d == "D":
                y -= v
            vertices.append((x, y))

    # The Schoelace Formula to evaluate polygon area
    A = 0
    for i in range(len(vertices)):
        if i == len(vertices) - 1:
            A += vertices[-1][0] * vertices[0][1]
            A -= vertices[-1][1] * vertices[0][0]
        else:
            A += vertices[i][0] * vertices[i + 1][1]
            A -= vertices[i][1] * vertices[i + 1][0]

    # Circuit has to have + 1, otherwise we will not count initial cell
    A = (abs(A) / 2) + (circuit / 2) + 1
    print(int(A))
