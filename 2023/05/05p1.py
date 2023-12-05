if __name__ == '__main__':

    maps = {}
    current_key = None
    keys = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location"
    ]
    seeds = []

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

    # print(seeds)
    # print(maps)

    results = []
    for seed in seeds:
        value = seed
        for key in keys:
            for mapping in maps[key]:
                dest, source, length = mapping
                if source <= value < source + length:
                    shift = value - source
                    value = dest + shift
                    break

        results.append(value)

    print(min(results))
