import functools


class Command:
    On = 1
    Off = 0

    def fromString(str):
        match str.lower():
            case "on":
                return Command.On
            case "off":
                return Command.Off
            case _:
                raise RuntimeError("Unknown string '{}' for command".format(str))


class Range:
    def __init__(self, frm, to):
        self.frm = frm
        self.to = to

    def fromString(str):
        return Range(*list(map(int, str.split(".."))))

    def __repr__(self):
        return "{}..{}".format(self.frm, self.to)

    def valid(self):
        return self.to >= self.frm

    def size(self):
        return self.to - self.frm + 1

    def overlap(self, other):
        return self.frm <= other.to and self.to >= other.frm


class Cuboid:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def fromString(dims):
        x = y = z = None
        for dim in dims.split(","):
            a, r = dim.split("=")
            match a:
                case "x":
                    x = Range.fromString(r)
                case "y":
                    y = Range.fromString(r)
                case "z":
                    z = Range.fromString(r)
                case _:
                    raise RuntimeError("Unknown dimension '{}'".format(a))

        if x is None or y is None or z is None:
            raise RuntimeError("Dimensions not all specified.")
        return Cuboid(x, y, z)

    def __repr__(self):
        return "(x:{} y:{} z:{})".format(self.x, self.y, self.z)

    def valid(self):
        return all(map(Range.valid, [self.x, self.y, self.z]))

    def size(self):
        return functools.reduce(
            lambda q, w: q * w, map(Range.size, [self.x, self.y, self.z])
        )

    def overlap(self, other):
        return all(
            map(Range.overlap, [self.x, self.y, self.z], [other.x, other.y, other.z])
        )


def remove(c, r):
    remain = []
    remain.append(Cuboid(Range(c.x.frm, r.x.frm - 1), c.y, c.z))  # To the left
    remain.append(Cuboid(Range(r.x.to + 1, c.x.to), c.y, c.z))  # To the right

    xr = Range(max(c.x.frm, r.x.frm), min(c.x.to, r.x.to))

    remain.append(Cuboid(xr, Range(c.y.frm, r.y.frm - 1), c.z))  # In front
    remain.append(Cuboid(xr, Range(r.y.to + 1, c.y.to), c.z))  # Behind

    yr = Range(max(c.y.frm, r.y.frm), min(c.y.to, r.y.to))

    remain.append(Cuboid(xr, yr, Range(c.z.frm, r.z.frm - 1)))  # Above
    remain.append(Cuboid(xr, yr, Range(r.z.to + 1, c.z.to)))  # Below

    return list(filter(Cuboid.valid, remain))


def part1(commands):
    grid = {}

    for cmd, cube in commands:
        if cube.x.to > 50 or cube.x.frm < -50:
            continue
        if cube.y.to > 50 or cube.y.frm < -50:
            continue
        if cube.z.to > 50 or cube.z.frm < -50:
            continue

        for x in range(cube.x.frm, cube.x.to + 1):
            for y in range(cube.y.frm, cube.y.to + 1):
                for z in range(cube.z.frm, cube.z.to + 1):
                    grid[(x, y, z)] = True if cmd == Command.On else False

    return list(grid.values()).count(True)


def part2(commands):
    on = []
    counts = []

    for cmd, cuboid in commands:
        on1 = [cuboid] if cmd == Command.On else []

        for i in on:
            if i.overlap(cuboid):
                on1 += remove(i, cuboid)
            else:
                on1.append(i)
        on = on1

        counts.append(sum([i.size() for i in on]))

    return counts[-1]


with open("input-22.txt", "r") as f:
    commands = list(
        map(
            lambda x: (Command.fromString(x[0]), Cuboid.fromString(x[1])),
            [line.strip().split(" ", 1) for line in f],
        )
    )

    print("Part 1:", part1(commands))
    print("Part 2:", part2(commands))
