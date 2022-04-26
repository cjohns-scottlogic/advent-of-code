from functools import reduce


def find_low_points(heightmap, rows, cols):
    low_points = []
    for r in range(0, rows):
        for c in range(0, cols):
            value = heightmap[r][c]

            above = heightmap[r - 1][c] if r > 0 else None
            below = heightmap[r + 1][c] if r < rows - 1 else None
            left = heightmap[r][c - 1] if c > 0 else None
            right = heightmap[r][c + 1] if c < cols - 1 else None

            others = filter(lambda x: x is not None, [above, below, left, right])
            if value < min(others):
                low_points.append(tuple([r, c, value]))

    return low_points


def find_basins(heightmap, rows, cols, low_points):
    basins = [[None for i in range(cols)] for j in range(rows)]

    def finder(r, c, x):
        if heightmap[r][c] == 9 or basins[r][c] is not None:
            return
        basins[r][c] = x
        if r > 0:
            finder(r - 1, c, x)
        if r < rows - 1:
            finder(r + 1, c, x)
        if c > 0:
            finder(r, c - 1, x)
        if c < cols - 1:
            finder(r, c + 1, x)

    x = 1
    for l in low_points:
        r, c, _ = l
        finder(r, c, x)
        x += 1

    return basins


with open("input-09.txt", "r") as f:
    rows = 0
    cols = None

    heightmap = []
    for line in [line.strip() for line in f]:
        heightrow = []
        for char in line:
            heightrow.append(int(char))
        if cols is None:
            cols = len(heightrow)
        elif cols != len(heightrow):
            raise RuntimeError("Column count mismatch")

        heightmap.append(heightrow)
        rows += 1

    low_points = find_low_points(heightmap, rows, cols)

    print("Part 1:", sum(map(lambda x: x[2], low_points)) + len(low_points))

    basins = find_basins(heightmap, rows, cols, low_points)

    basin_map = {}

    for r in range(rows):
        for c in range(cols):
            basin = basins[r][c]
            if basin:
                if basin not in basin_map:
                    basin_map[basin] = 1
                else:
                    basin_map[basin] += 1

    print(
        "Part 2: {}".format(reduce(lambda p, c: p * c, sorted(basin_map.values())[-3:]))
    )
