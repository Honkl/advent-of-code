from typing import List


def parse_values(line: str) -> int:
    return int("".join([v.strip() for v in line.split(":")[1].split(" ") if v != ""]))


if __name__ == '__main__':
    with open("input.txt", "r", encoding="utf-8") as f:
        time = parse_values(f.readline())
        distance = parse_values(f.readline())

    n_wins = 0
    for ms in range(1, time):
        if (time - ms) * ms > distance:
            n_wins += 1

    print(n_wins)
