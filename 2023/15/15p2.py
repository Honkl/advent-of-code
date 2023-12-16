def hash_f(sequence: str) -> int:
    value = 0
    for ch in sequence:
        value = ((value + ord(ch)) * 17) % 256
    return value


if __name__ == '__main__':
    with open("input.txt") as f:
        line = f.readline().strip()
        steps = line.split(",")

    boxes = {i: [] for i in range(256)}

    for step in steps:
        sign = "=" if "=" in step else "-"
        code, f_length = step.split(sign)
        box = hash_f(code)

        if sign == "-":
            index = None
            for i, item in enumerate(boxes[box]):
                if item[0] == code:
                    index = i
                    break
            if index is not None:
                del boxes[box][index]

        if sign == "=":
            found = False
            for i, item in enumerate(boxes[box]):
                if item[0] == code:
                    boxes[box][i] = (code, f_length)
                    found = True
                    break

            if not found:
                boxes[box].append((code, f_length))

    total = 0
    for box, lenses in boxes.items():
        for order, lens in enumerate(lenses):
            total += (1 + box) * (1 + order) * (int(lens[1]))

    print(total)

