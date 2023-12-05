from collections import namedtuple
from typing import Dict, List, Tuple

keys = [
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location"
]


class Node(namedtuple):
    start: int
    end: int
    level: str


def load_data() -> Tuple[Dict[str, List[List[int]]], Dict[int, int]]:
    maps = {}
    current_key = None
    seeds = []

    with open("input_test.txt", "r", encoding="utf-8") as f:
        for line in f:

            if "seeds" in line:
                seeds = list(map(int, line.split(":")[1].strip().split(" ")))
                continue

            for key in keys:
                if key in line:
                    current_key = key
                    break

            if "map" in line or line.strip() == "":
                continue

            if current_key not in maps.keys():
                maps[current_key] = []

            data = list(map(int, line.strip().split(" ")))
            maps[current_key].append(data)

    # Convert seeds to actual list
    new_seeds = {}
    for i, s in enumerate(seeds):
        if i % 2 == 0:
            new_seeds[s] = seeds[i + 1]

    return maps, new_seeds


maps, seeds = load_data()


def resolve(node: Node) -> List[Node] | int:
    insatiable, satiable = [], []
    for mapping in maps[node.level]:
        dest, source, length = mapping

        # Whole number is out of bounds
        if node.end < source or node.start > dest:
            continue

        # Number partially belongs to the range
        satiable.append(Node(
            max(node.start, source),
            min(node.end, source + length - 1),
            node.level,
        ))

    for sat_node in satiable:
        ...
        # TODO: some nice logic


if __name__ == '__main__':

    results = []
    nodes_to_process = []
    for seed, length_ in seeds.items():
        nodes_to_process.append(Node(seed, seed + length_ - 1, "seed-to-soil"))

    min_location = None
    while len(nodes_to_process) > 0:
        n = nodes_to_process.pop(0)
        result = resolve(n)
        if isinstance(result, int):
            if min_location is None or result < min_location:
                min_location = result
        else:
            nodes_to_process.append(result)

    print(min_location)
