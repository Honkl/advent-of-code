def hash_f(sequence: str) -> int:
    value = 0
    for ch in sequence:
        value = ((value + ord(ch)) * 17) % 256
    return value


if __name__ == '__main__':
    with open("input.txt") as f:
        line = f.readline().strip()
        steps = line.split(",")

    print(sum(hash_f(step) for step in steps))
