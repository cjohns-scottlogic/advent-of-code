def part1(positions):
    best = None
    for p in range(max(positions) + 1):
        fuel = 0
        for c in positions:
            fuel += abs(c - p)
        if not best or fuel < best:
            best = fuel

    return best


def part2(positions):
    best = None
    lookup = {}

    for p in range(max(positions) + 1):
        fuel = 0
        for c in positions:
            count = abs(c - p)
            if count not in lookup:
                r = 0
                for i in range(count):
                    r += i + 1
                lookup[count] = r
            fuel += lookup[count]
        if not best or fuel < best:
            best = fuel

    return best


with open("input-07.txt", "r") as f:
    positions = [int(x) for x in f.read().split(",")]

    print("Part 1:", part1(positions))
    print("Part 2:", part2(positions))
