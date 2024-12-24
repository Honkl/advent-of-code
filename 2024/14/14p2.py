import os
import timeit

width = 101
height = 103

Robot = tuple[tuple[int, int], tuple[int, int]]


def move(robot: Robot, steps: int) -> Robot:
    x, y = robot[0]
    vx, vy = robot[1]

    new_x = (steps * vx) + x
    if new_x < 0:
        new_x = (width - (-new_x % width)) % width
    else:
        new_x = new_x % width

    new_y = (steps * vy) + y
    if new_y < 0:
        new_y = (height - (-new_y % height)) % height
    else:
        new_y = new_y % height

    return (new_x, new_y), (vx, vy)


def visualize(robots: list[Robot]) -> str:
    result = ""

    for i in range(height):
        row = []
        for j in range(width):
            count = 0
            for r in robots:
                if r[0] == (j, i):
                    count += 1
            if count > 0:
                row.append(str(count))
            else:
                row.append(".")
        result += "".join(row) + "\n"

    return result


def hash_robots(robots: list[Robot]) -> str:
    result = []
    for r in robots:
        result.append(str(r[0][0]))
        result.append(str(r[0][1]))

    return "".join(result)


def run() -> None:
    robots = []
    with open("input.txt", "r") as f:
        for line in f:
            position, velocity = line.split(" ")
            position = position.split("=")[1].strip()
            position = (
                int(position.split(",")[0]),
                int(position.split(",")[1]),
            )
            velocity = velocity.split("=")[1].strip()
            velocity = (
                int(velocity.split(",")[0]),
                int(velocity.split(",")[1]),
            )
            robots.append((position, velocity))

    seen_patterns = []

    # Shift before iteration starts
    # for i in range(len(robots)):
    #     robots[i] = move(robots[i], steps=8258)

    # Total number of allocations is 10403 until it repeats itself
    # iterating through positions, printing them, looking for the tree in terminal
    for step in range(1000):

        for i in range(len(robots)):
            robots[i] = move(robots[i], steps=1)

        output = visualize(robots)
        os.system('cls')
        print(f"Step: {step}")
        print(output)

        h = hash_robots(robots)

        if h in seen_patterns:
            break
        else:
            seen_patterns.append(h)

    print(len(seen_patterns))
    output = visualize(robots)
    print(output)


if __name__ == '__main__':
    start = timeit.default_timer()
    run()
    print(f"Runtime: {timeit.default_timer() - start}s")
