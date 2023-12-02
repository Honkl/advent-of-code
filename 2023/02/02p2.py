import typing as t
from functools import reduce

config = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

colors = ["red", "green", "blue"]

Game = t.List[t.Dict[str, int]]


def is_feasible(game: Game) -> bool:
    for round in game:
        for color in colors:
            if round[color] > config[color]:
                return False
    return True


def find_min_power(game: Game) -> int:
    max_value = {c: 0 for c in colors}
    for round in game:
        for c in colors:
            max_value[c] = max(max_value[c], round[c])
    return reduce(lambda x, y: x * y, max_value.values())


def parse(line: str) -> Game:
    result = []
    games = line.split(":")[1]
    for game in games.split(";"):

        counts = {c: 0 for c in colors}

        for part in game.split(","):
            number, color, *_ = part.strip().split(" ")
            counts[color] = int(number)

        result.append(counts)

    return result


if __name__ == '__main__':

    total = 0
    with open("input.txt", "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            game = parse(line)
            feasible = is_feasible(game)
            power = find_min_power(game)
            # print(f"Game {i + 1}: Feasible={feasible}, Power={power}")
            total += power

    print(total)
