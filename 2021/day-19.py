from scipy.spatial.transform import Rotation
from itertools import product
from functools import partial


class Beacon:
    def fromString(loc):
        return Beacon([int(x) for x in loc.split(",")])

    def __init__(self, xyz):
        self.x, self.y, self.z = xyz

    def __repr__(self):
        return "{},{},{}".format(self.x, self.y, self.z)


def offset(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def rotate_beacon(i, beacon):
    x, y, z = beacon.x, beacon.y, beacon.z
    return Beacon(
        [
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


rotations = [
    Rotation.from_euler("xyz", [0, 0, 0], degrees=True),
    Rotation.from_euler("xyz", [90, 0, 0], degrees=True),
    Rotation.from_euler("xyz", [180, 0, 0], degrees=True),
    Rotation.from_euler("xyz", [-90, 0, 0], degrees=True),
    Rotation.from_euler("xyz", [0, 90, 0], degrees=True),
    Rotation.from_euler("xyz", [90, 90, 0], degrees=True),
    Rotation.from_euler("xyz", [180, 90, 0], degrees=True),
    Rotation.from_euler("xyz", [-90, 90, 0], degrees=True),
    Rotation.from_euler("xyz", [0, -90, 0], degrees=True),
    Rotation.from_euler("xyz", [90, -90, 0], degrees=True),
    Rotation.from_euler("xyz", [180, -90, 0], degrees=True),
    Rotation.from_euler("xyz", [-90, -90, 0], degrees=True),
    Rotation.from_euler("xyz", [0, 0, 90], degrees=True),
    Rotation.from_euler("xyz", [90, 0, 90], degrees=True),
    Rotation.from_euler("xyz", [180, 0, 90], degrees=True),
    Rotation.from_euler("xyz", [-90, 0, 90], degrees=True),
    Rotation.from_euler("xyz", [0, 0, 180], degrees=True),
    Rotation.from_euler("xyz", [90, 0, 180], degrees=True),
    Rotation.from_euler("xyz", [180, 0, 180], degrees=True),
    Rotation.from_euler("xyz", [-90, 0, 190], degrees=True),
    Rotation.from_euler("xyz", [0, 0, -90], degrees=True),
    Rotation.from_euler("xyz", [90, 0, -90], degrees=True),
    Rotation.from_euler("xyz", [180, 0, -90], degrees=True),
    Rotation.from_euler("xyz", [-90, 0, -90], degrees=True),
]

x = []
for r in rotations:
    q, w, e = r.apply([[5, 7, 9]])[0]
    p = (int(q), int(w), int(e))
    x.append(p)

for z in x:
    q = [abs(z[0]), abs(z[1]), abs(z[2])]
    q.sort()
    if q != [5, 7, 9]:
        print(q)


class Scanner:
    def __init__(self, number):
        self.number = number
        self.position = (0, 0, 0) if number == 0 else None
        self.beacons = set()

    def __repr__(self):
        return "{} at {}".format(
            self.number,
            self.position if self.position else "unknown",
        )

    @property
    def located(self):
        return self.position is not None


with open("test-19.txt", "r") as f:
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
        unknowns = list(filter(lambda x: not x[1].located, scanners.items()))
        if len(unknowns) == 0:
            break

        for candidate in unknowns:
            # Try each rotation
            # for rotation in rotations:
            #    test = list(
            #        map(
            #            lambda t: (int(t[0]), int(t[1]), int(t[2])),
            #            rotation.apply(list(candidate[1].beacons)),
            #        )
            #    )
            for rix in range(24):
                beacons = set(
                    map(
                        partial(rotate_beacon, rix),
                        candidate[1].beacons,
                    )
                )

                # Match it against each known scanner
                for known in filter(lambda x: x[1].located, scanners.items()):

                    deltamap = {}  # Delta -> Count
                    # Find the differences for each beacon
                    for kb in known[1].beacons:
                        for cb in beacons:
                            delta = (kb.x - cb.x, kb.y - cb.y, kb.z - cb.z)
                            if delta not in deltamap:
                                deltamap[delta] = 1
                            else:
                                deltamap[delta] += 1

                    found = list(filter(lambda x: x[1] >= 12, deltamap.items()))
                    if len(found) > 0:
                        # We now have the offset and rotation to match this scanner
                        delta, _ = found[0]
                        print(
                            "Matched scanner {} with rotation {} with known scanner {} offset {}".format(
                                candidate[0],
                                rix,  #  was rotations.index(rotation)
                                known[0],
                                delta,
                            )
                        )

                        scanner = candidate[1]
                        scanner.position = offset(delta, known[1].position)
                        scanner.beacons = beacons
                        break

    beacons = set()
    for scanner in scanners.values():
        beacons = beacons.union(
            set(
                map(
                    partial(offset, scanner.position),
                    map(lambda x: (x.x, x.y, x.z), scanner.beacons),
                )
            )
        )
        print(scanner)
        print(scanner.beacons)

    print(len(beacons))
