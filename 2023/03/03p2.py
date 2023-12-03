import re
import typing as t
from collections import namedtuple

Number = namedtuple("Number", ["value", "start", "end", "row"])
Symbol = namedtuple("Symbol", ["value", "row", "column"])


def is_adjacent(number: Number, symbol: Symbol) -> bool:
    if symbol.row in [number.row - 1, number.row, number.row + 1]:
        if number.start - 1 <= symbol.column <= number.end + 1:
            return True
    return False


def gear_score(sym: Symbol, numbers: t.List[Number]) -> int:  # noqa
    if sym.value != "*":
        return 0

    ads = [n for n in numbers if is_adjacent(n, sym)]
    if len(ads) == 2:
        return ads[0].value * ads[1].value

    return 0


if __name__ == '__main__':

    regex = "\\d+"
    pattern = re.compile(regex)

    numbers, symbols = [], []

    with open("input.txt", "r", encoding="utf-8") as f:
        for i, line in enumerate(f):

            for j, ch in enumerate(line.strip()):
                if ch != "." and not str(ch).isnumeric():
                    symbols.append(Symbol(ch, i, j))

            match = pattern.search(line)
            if match is None:
                continue

            while match:
                numbers.append(Number(int(match.group()), match.start(), match.end() - 1, i))
                match = pattern.search(line, match.end())

    total = 0
    for s in symbols:
        total += gear_score(s, numbers)

    print(total)
