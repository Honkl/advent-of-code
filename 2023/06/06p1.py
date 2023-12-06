from typing import List


def parse_values(line: str) -> List[int]:
    return [int(v.strip()) for v in line.split(":")[1].split(" ") if v != ""]


if __name__ == '__main__':
    with open("input.txt", "r", encoding="utf-8") as f:
        times = parse_values(f.readline())
        distances = parse_values(f.readline())

    result = 1
    for race_index in range(len(times)):
        n_wins = 0
        for ms in range(1, times[race_index]):
            if (times[race_index] - ms) * ms > distances[race_index]:
                n_wins += 1
        result *= n_wins

    print(result)
