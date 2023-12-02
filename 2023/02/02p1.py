import typing as t

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
            if is_feasible(game):
                total += i + 1

    print(total)
