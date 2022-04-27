from functools import reduce

with open("input-13.txt", "r") as f:
    points = set()
    commands = []
    reading_points = True
    for line in [line.strip() for line in f]:
        if line == "":
            reading_points = False
        else:
            if reading_points:
                points.add(tuple([int(x) for x in line.split(",")]))
            else:
                commands.append(line.split()[2].split("="))

    for axis, value in commands:
        value = int(value)
        if axis == "y":
            for point in list(points):
                if point[1] > value:
                    points.add((point[0], value - (point[1] - value)))
                    points.remove(point)

        if axis == "x":
            for point in list(points):
                if point[0] > value:
                    points.add((value - (point[0] - value), point[1]))
                    points.remove(point)

        print("Fold on {} {} : {} points.".format(axis, value, len(points)))

    max_x = reduce(max, [point[0] for point in points]) + 1
    max_y = reduce(max, [point[1] for point in points]) + 1

    print("")
    for y in range(0, max_y):
        line = ""
        for x in range(0, max_x):
            line += "#" if (x, y) in points else " "
        print(line)
