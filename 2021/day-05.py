def add_point(points, row, col):
    if (row, col) not in points:
        points[(row, col)] = 1
    else:
        points[(row, col)] += 1


with open("input-05.txt", "r") as f:
    points_1 = {}
    points_2 = {}
    for line in f:
        line = line.strip()
        start, _, end = line.split()
        x1, y1 = [int(x) for x in start.split(",")]
        x2, y2 = [int(x) for x in end.split(",")]
        if x1 == x2:
            for row in range(min(y1, y2), max(y1, y2) + 1):
                add_point(points_1, x1, row)
                add_point(points_2, x1, row)
        elif y1 == y2:
            for col in range(min(x1, x2), max(x1, x2) + 1):
                add_point(points_1, col, y1)
                add_point(points_2, col, y1)
        else:
            col, row = x1, y1
            while col != x2 or row != y2:
                add_point(points_2, col, row)
                col += 1 if x2 > x1 else -1
                row += 1 if y2 > y1 else -1
            add_point(points_2, col, row)

    print("Part 1:", len(list(filter(lambda v: v > 1, points_1.values()))))
    print("Part 2:", len(list(filter(lambda v: v > 1, points_2.values()))))
