from multiprocessing import Pool
from typing import Tuple

keys = [
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location"
]

maps = {}

with open("input.txt", "r", encoding="utf-8") as f:
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


def resolve(node: Tuple[int, int]) -> int:
    print(f"Called resolve with node: {node}")
    min_value = None
    for seed in range(node[0], node[0] + node[1]):
        value = seed
        for key in keys:
            for mapping in maps[key]:
                dest, source, length = mapping
                if source <= value < source + length:
                    shift = value - source
                    value = dest + shift
                    break

        if min_value is None or value < min_value:
            min_value = value

    print(f"Node {node} resolved with min value {min_value}")
    return min_value


if __name__ == '__main__':

    # Use PyPy3 to bruteforce
    # Run pypy.exe .\05p2_bruteforce.py

    current_key = None
    new_seeds = []
    for i, s in enumerate(seeds):
        if i % 2 == 0:
            new_seeds.append((s, seeds[i + 1]))

    with Pool(16) as p:
        results = p.map(resolve, new_seeds)

    print(min(results))
