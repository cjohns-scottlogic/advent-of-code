def part1(data):
    ages = data.copy()
    for _ in range(80):
        new = 0
        for i in range(0, len(ages)):
            if ages[i] == 0:
                ages[i] = 6
                new += 1
            else:
                ages[i] -= 1
        ages += [8] * new

    return len(ages)


def run(data, iterations):
    ages = [0] * 9

    for age in data:
        ages[age] += 1

    for n in range(iterations):
        new = ages[0]
        for i in range(0, 8):
            ages[i] = ages[i + 1]
        ages[8] = new
        ages[6] += new

    return sum(ages)


with open("input-06.txt", "r") as f:
    data = [int(x) for x in f.read().split(",")]

    # print("Part 1:", part1(data))
    print("Part 1:", run(data, 80))
    print("Part 2:", run(data, 256))
