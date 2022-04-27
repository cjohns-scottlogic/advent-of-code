from numpy import array
from itertools import product


def step(data):
    flashes = 0
    for x, y in product(range(10), range(10)):
        data[x][y] += 1

    flashed = True
    while flashed:
        flashed = False
        for x, y in product(range(10), range(10)):
            if data[x][y] > 9:
                flashed = True
                flashes += 1
                data[x][y] = -1
                if x > 0 and data[x - 1][y] != -1:
                    data[x - 1][y] += 1
                if x < 9 and data[x + 1][y] != -1:
                    data[x + 1][y] += 1
                if y > 0 and data[x][y - 1] != -1:
                    data[x][y - 1] += 1
                if y < 9 and data[x][y + 1] != -1:
                    data[x][y + 1] += 1
                if x > 0 and y > 0 and data[x - 1][y - 1] != -1:
                    data[x - 1][y - 1] += 1
                if x < 9 and y > 0 and data[x + 1][y - 1] != -1:
                    data[x + 1][y - 1] += 1
                if x > 0 and y < 9 and data[x - 1][y + 1] != -1:
                    data[x - 1][y + 1] += 1
                if x < 9 and y < 9 and data[x + 1][y + 1] != -1:
                    data[x + 1][y + 1] += 1

    flashed = 0
    for x, y in product(range(10), range(10)):
        if data[x][y] == -1:
            flashed += 1
            data[x][y] = 0

    return flashes, flashed


def part1(data):
    flashes = 0

    for _ in range(100):
        flashes += step(data)[0]

    return flashes


def part2(data):
    s = 0

    while True:
        s += 1
        _, flashed = step(data)
        if flashed == 100:
            break

    return s


with open("input-11.txt", "r") as f:
    data = []
    for line in [line.strip() for line in f]:
        data.append([int(c) for c in line])

    data = array(data)
    print("Part 1:", part1(data.copy()))
    print("Part 2:", part2(data.copy()))
