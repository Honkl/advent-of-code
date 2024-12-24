import timeit

width = 101
height = 103
steps = 100

Robot = tuple[tuple[int, int], tuple[int, int]]


def move(robot: Robot) -> Robot:
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


def safety_factor(robots: list[Robot]) -> int:
    mid_x = int(width / 2)
    mid_y = int(height / 2)

    top_left, top_right = 0, 0
    bottom_left, bottom_right = 0, 0

    for r in robots:
        x, y = r[0]
        if x < mid_x and y < mid_y:
            top_left += 1
        elif x < mid_x and y > mid_y:
            bottom_left += 1
        elif x > mid_x and y < mid_y:
            top_right += 1
        elif x > mid_x and y > mid_y:
            bottom_right += 1

    return top_left * top_right * bottom_left * bottom_right


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

    for i in range(len(robots)):
        robots[i] = move(robots[i])

    factor = safety_factor(robots)
    print(f"Total: {factor}")


if __name__ == '__main__':
    start = timeit.default_timer()
    run()
    print(f"Runtime: {timeit.default_timer() - start}s")
