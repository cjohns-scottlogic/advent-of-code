def find_paths(cavemap, paths, cave, search, small2):
    s1 = search + [cave]
    for x in cavemap[cave]:
        if x == "start":
            continue
        elif x == "end":
            if s1 not in paths:
                paths.append(s1)
        elif x.islower() and x in search:
            if x == small2:
                find_paths(cavemap, paths, x, s1, None)
            else:
                continue
        else:
            find_paths(cavemap, paths, x, s1, small2)


def part1(cavemap):
    paths = []
    find_paths(cavemap, paths, "start", [], None)
    return len(paths)


def part2(cavemap):
    paths = []
    for sc in filter(lambda x: x.islower() and x not in ["start", "end"], cavemap):
        print("Visting cave {} twice...".format(sc))
        find_paths(cavemap, paths, "start", [], sc)
    return len(paths)


with open("input-12.txt", "r") as f:
    cavemap = {}
    for a, b in [line.strip().split("-") for line in f]:
        if a not in cavemap:
            cavemap[a] = [b]
        else:
            cavemap[a].append(b)

        if b not in cavemap:
            cavemap[b] = [a]
        else:
            cavemap[b].append(a)

    print("Part 1:", part1(cavemap))
    print("Part 2:", part2(cavemap))
