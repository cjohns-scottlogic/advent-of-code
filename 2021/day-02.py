def part1(commands):
    horizontal = 0
    depth = 0
    for (cmd, val) in commands:
        if cmd == "forward":
            horizontal += val
        elif cmd == "up":
            depth -= val
        elif cmd == "down":
            depth += val

    return horizontal * depth


def part2(commands):
    horizontal = 0
    depth = 0
    aim = 0
    for (cmd, val) in commands:
        if cmd == "forward":
            horizontal += val
            depth += aim * val
        elif cmd == "up":
            aim -= val
        elif cmd == "down":
            aim += val

    return horizontal * depth


with open("input-02.txt", "r") as f:
    commands = list(
        map(lambda item: (item[0], int(item[1])), [line.strip().split() for line in f])
    )

    print("Part 1:", part1(commands))
    print("Part 2:", part2(commands))
