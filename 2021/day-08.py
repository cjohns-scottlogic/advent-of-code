def part1(data):
    counts = {}
    for n in range(1, 8):
        counts[n] = 0

    for _, vals in data:
        for val in vals:
            counts[len(val)] += 1

    return counts[2] + counts[3] + counts[4] + counts[7]


def part2(data):
    sum = 0
    for segs, vals in data:
        segs = [set(x) for x in segs]
        segmap = {}
        # Find the easy ones
        for seg in segs:
            if len(seg) == 2:
                segmap[1] = seg
            if len(seg) == 3:
                segmap[7] = seg
            if len(seg) == 4:
                segmap[4] = seg
            if len(seg) == 7:
                segmap[8] = seg
        unknown = list(filter(lambda v: v not in segmap.values(), segs))

        # Figure out what is at the bottom. It's common to the others, but not in 7
        bottom = None
        for letter in "abcdefg":
            if all(map(lambda x: letter in x, unknown)):
                if letter not in segmap[7]:
                    if bottom is not None:
                        raise RuntimeError("Huh?!")
                    bottom = letter

        # 9 is whatever is in 7, 4 and the bottom
        nine = segmap[4].union(segmap[7]).union(set([bottom]))
        segmap[9] = nine

        # Filter out the ones we now know
        unknown = list(filter(lambda v: v not in segmap.values(), segs))

        # The bottom-left element is in 8 but not 9
        bottom_left = segmap[8].difference(segmap[9])

        # There are three items left with 5 segments on: 2, 3 and 5
        # 1 is a subset of 3, 2 has the bottom-left segment on
        for item in filter(lambda v: len(v) == 5, unknown):
            if segmap[1].issubset(item):
                segmap[3] = item
            elif bottom_left.issubset(item):
                segmap[2] = item
            else:
                segmap[5] = item

        # There are two items left with 6 segments on: 0 and 6
        # 1 is a subset of 0
        for item in filter(lambda v: len(v) == 6, unknown):
            if segmap[1].issubset(item):
                segmap[0] = item
            else:
                segmap[6] = item

        # Filter out the ones we now know
        unknown = list(filter(lambda v: v not in segmap.values(), segs))

        lookup = {}
        for value, segs in segmap.items():
            key = "".join(sorted(list(segs)))
            if key in lookup:
                raise RuntimeError("Duplicate key")
            lookup[key] = value

        value = 0
        for val in vals:
            value = (value * 10) + lookup["".join(sorted(val))]

        sum += value

    return sum


with open("input-08.txt", "r") as f:
    data = list(
        map(
            lambda line: (line[0].strip().split(), line[1].strip().split()),
            [line.strip().split("|") for line in f],
        )
    )

    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
