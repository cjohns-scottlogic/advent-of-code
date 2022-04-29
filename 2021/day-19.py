from functools import partial
from itertools import product
from tabnanny import verbose


class Point:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __repr__(self):
        return "{},{},{}".format(self.x, self.y, self.z)

    def xyz(self):
        return (self.x, self.y, self.z)

    def offset(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)


class Beacon(Point):
    def fromString(loc):
        return Beacon(*[int(x) for x in loc.split(",")])

    def rotate(self, i):
        x, y, z = self.xyz()
        return Beacon(
            *[
                (x, y, z),
                (z, y, -x),
                (-x, y, -z),
                (-z, y, x),
                (-x, -y, z),
                (-z, -y, -x),
                (x, -y, -z),
                (z, -y, x),
                (x, -z, y),
                (y, -z, -x),
                (-x, -z, -y),
                (-y, -z, x),
                (x, z, -y),
                (-y, z, -x),
                (-x, z, y),
                (y, z, x),
                (z, x, y),
                (y, x, -z),
                (-z, x, -y),
                (-y, x, z),
                (-z, -x, y),
                (y, -x, z),
                (z, -x, -y),
                (-y, -x, -z),
            ][i]
        )


class Scanner:
    def __init__(self, number):
        self.number = number
        self.position = Point(0, 0, 0) if number == 0 else None
        self.beacons = set()

    def __repr__(self):
        return "{} at {}".format(
            self.number,
            self.position if self.position else "unknown",
        )

    @property
    def located(self):
        return self.position is not None


with open("input-19.txt", "r") as f:
    verbose = False
    scanners = {}
    for line in [line.strip() for line in f]:
        if len(line) > 0:
            if line.startswith("---"):
                sn = int(line.split()[2])
                scanners[sn] = Scanner(sn)
            else:
                scanners[sn].beacons.add(Beacon.fromString(line))

    # For each scanner we're trying to match
    while True:
        unknowns = list(filter(lambda x: not x.located, scanners.values()))
        if len(unknowns) == 0:
            break

        for candidate in unknowns:
            for rix in range(24):
                beacons = set()
                for beacon in candidate.beacons:
                    beacons.add(beacon.rotate(rix))

                # Match it against each known scanner
                for known in filter(lambda x: x.located, scanners.values()):
                    deltamap = {}  # Delta -> Count

                    # Find the differences for each beacon
                    for kb in known.beacons:
                        for cb in beacons:
                            delta = (kb.x - cb.x, kb.y - cb.y, kb.z - cb.z)
                            if delta not in deltamap:
                                deltamap[delta] = 1
                            else:
                                deltamap[delta] += 1

                    found = list(
                        map(
                            lambda x: x[0],
                            filter(lambda x: x[1] >= 12, deltamap.items()),
                        )
                    )
                    if len(found) > 0:
                        # We now have the offset and rotation to match this scanner
                        delta = Point(*found[0])
                        if verbose:
                            print(
                                "Matched scanner {} with rotation {} with known scanner {} offset {}".format(
                                    candidate.number,
                                    rix,
                                    known.number,
                                    delta,
                                )
                            )

                        scanner = candidate
                        scanner.position = known.position.offset(delta)
                        scanner.beacons = beacons
                        break

    beacons = set()
    for scanner in scanners.values():
        beacons = beacons.union(
            set(
                map(scanner.position.offset, scanner.beacons),
            )
        )
    print("Part 1:", len(beacons))

    def manhattan(a, b):
        return a.x - b.x + a.y - b.y + a.z - b.z

    furthest = 0

    for s1, s2 in product(scanners.values(), scanners.values()):
        furthest = max(manhattan(s1.position, s2.position), furthest)

    print("Part 2:", furthest)
