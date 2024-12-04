import re

if __name__ == '__main__':
    with open("input.txt", "r") as f:
        line = "\n".join(f.readlines())

    pattern = r"mul\([\d]{1,3},[\d]{1,3}\)"

    total = 0
    enabled = True

    matches = re.findall(pattern, line)

    while len(matches) > 0:
        if line.startswith(matches[0]):
            if enabled:
                first, second = matches[0].replace("mul(", "").replace(")", "").split(",")
                total += int(first) * int(second)
            matches.pop(0)

        if line.startswith("do()"):
            enabled = True
        if line.startswith("don't()"):
            enabled = False

        line = line[1:]

    print(total)
