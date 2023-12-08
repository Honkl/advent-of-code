import math

if __name__ == '__main__':

    instructions = []
    patterns = {}
    with open("input.txt", "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i == 0:
                instructions = line.strip()
            if i > 1:
                source, others = line.split("=")
                left, right = others.replace("(", "").replace(")", "").split(", ")
                patterns[source.strip()] = (left.strip(), right.strip())

    states = [s for s in patterns.keys() if s[-1] == "A"]

    required_steps = []
    for s in states:
        index = 0
        steps = 0
        state = s
        while state[-1] != "Z":
            direction = 0 if instructions[index] == "L" else 1
            state = patterns[state][direction]
            index += 1
            if index >= len(instructions):
                index = 0
            steps += 1

        required_steps.append(steps)

    print(math.lcm(*required_steps))
