def part1(data):
    gamma = ""
    epsilon = ""
    for x in range(0, len(data[0])):
        ones = 0
        zeros = 0
        for item in data:
            if item[x] == "1":
                ones += 1
            elif item[x] == "0":
                zeros += 1

        if ones > zeros:
            gamma += "1"
            epsilon += "0"
        elif zeros > ones:
            gamma += "0"
            epsilon += "1"

    return int(gamma, 2) * int(epsilon, 2)


def find_value(data, flag):
    if len(data) == 1:
        return data[0]
    ones = []
    zeros = []
    for item in data:
        if item[0] == "1":
            ones.append(item[1:])
        elif item[0] == "0":
            zeros.append(item[1:])

    if not flag:
        if len(ones) > len(zeros):
            return "1" + find_value(ones, flag)
        if len(zeros) > len(ones):
            return "0" + find_value(zeros, flag)
        return "1" + find_value(ones, flag)

    if flag:
        if len(ones) < len(zeros):
            return "1" + find_value(ones, flag)
        if len(zeros) < len(ones):
            return "0" + find_value(zeros, flag)
        return "0" + find_value(zeros, flag)


def part2(data):
    o2_gen = find_value(data, False)
    co2_scrub = find_value(data, True)

    return int(o2_gen, 2) * int(co2_scrub, 2)


with open("input-03.txt", "r") as f:
    data = [line.strip() for line in f]

    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
