import re

if __name__ == '__main__':
    with open("input.txt", "r") as f:
        lines = f.readlines()

    pattern = r"mul\([\d]{1,3},[\d]{1,3}\)"

    total = 0
    for line in lines:
        for match in re.findall(pattern, line):
            first, second = match.replace("mul(", "").replace(")", "").split(",")
            total += int(first) * int(second)

    print(total)
