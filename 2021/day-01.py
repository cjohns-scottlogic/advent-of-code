def part1(data):
    last = None
    increments = 0
    for i in data:
        if last and i > last:
            increments += 1
        last = i
    return increments


def part2(data):
    last_sum = None
    increases = 0
    for i in range(len(data) - 2):
        window = data[i : i + 3]
        this_sum = sum(window)
        if last_sum and this_sum > last_sum:
            increases += 1
        last_sum = this_sum
    return increases


with open("input-01.txt", "r") as f:
    data = [int(l.strip()) for l in f]

    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
