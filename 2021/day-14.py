import itertools


def part1(polymer, rules):
    for _ in range(0, 10):
        new_poly = polymer[0]
        for x in range(0, len(polymer) - 1):
            z = polymer[x : x + 2]
            ins = rules[(z[0], z[1])]
            new_poly += ins + z[1]

        polymer = new_poly

    freq_map = {}
    for c in polymer:
        if c not in freq_map:
            freq_map[c] = 1
        else:
            freq_map[c] += 1

    return max(freq_map.values()) - min(freq_map.values())


def part2(polymer, rules):
    pairs = {}
    for r in rules:
        pairs[(r[0], r[1])] = 0

    for x in itertools.pairwise(polymer):
        pairs[x] += 1

    for _ in range(0, 40):
        for pair, count in list(pairs.items()):
            ins = rules[pair]
            pairs[(pair[0], ins)] += count
            pairs[(ins, pair[1])] += count
            pairs[pair] -= count

    freq_map = {}

    for pair, count in pairs.items():
        for c in pair:
            if c not in freq_map:
                freq_map[c] = count
            else:
                freq_map[c] += count

    for x in freq_map:
        freq_map[x] = int((freq_map[x] + 1) / 2)

    return max(freq_map.values()) - min(freq_map.values())


with open("input-14.txt", "r") as f:
    polymer = f.readline().strip()
    rules = {}

    for line in filter(len, [line.strip() for line in f]):
        r, t = line.split(" -> ")
        rules[(r[0], r[1])] = t

    print("Part 1:", part1(polymer, rules))
    print("Part 2:", part2(polymer, rules))
