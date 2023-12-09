from typing import List


def score(sequence: List[int]) -> int:
    temp_sequences = [sequence]
    s = sequence
    while any(v != 0 for v in s):
        s = [s[i + 1] - s[i] for i in range(len(s) - 1)]
        temp_sequences.append(s)

    addition = 0
    for s in reversed(temp_sequences):
        addition = s[-1] + addition

    return addition


if __name__ == '__main__':
    with open("input.txt", "r") as f:
        sequences = [list(map(int, line.split(" "))) for line in f]

    print(sum([score(s) for s in sequences]))
