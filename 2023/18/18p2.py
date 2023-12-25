if __name__ == '__main__':

    vertices = []
    x, y = 0, 0
    circuit = 0
    with open("input.txt", "r") as f:
        for line in f:
            _, _, code = line.strip().split(" ")

            v = int(code[2:7], 16)
            d = code[7]

            v = int(v)
            circuit += v

            if d == "0":
                x += v
            if d == "2":
                x -= v
            if d == "3":
                y += v
            if d == "1":
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
