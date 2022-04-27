import numpy
import itertools


def part1(risk, size):
    best = numpy.zeros((size, size), numpy.int32)
    best[0, 0] = 1

    changed = True

    while changed:
        changed = False
        for r, c in itertools.product(range(size), range(size)):
            if best[r, c] == 0:
                continue

            def check_cell(x, r1, c1):
                b = x + risk[r1, c1]
                if best[r1, c1] == 0 or b < best[r1, c1]:
                    best[r1, c1] = b
                    return True
                return False

            b = best[r, c]
            h = [False] * 4
            if c > 0:
                h[0] = check_cell(b, r, c - 1)
            if c < size - 1:
                h[1] = check_cell(b, r, c + 1)
            if r > 0:
                h[2] = check_cell(b, r - 1, c)
            if r < size - 1:
                h[3] = check_cell(b, r + 1, c)
            changed = changed or any(h)

    return best[size - 1, size - 1] - 1


def part2(risk1, size):
    risk = numpy.zeros((size * 5, size * 5), numpy.int32)

    for t in range(0, 5):
        if t == 0:
            for r, c in itertools.product(range(size), range(size)):
                risk[r][c] = risk1[r][c]
        else:
            for r, c in itertools.product(range(size), range(size)):
                nr = risk[size * (t - 1) + r, c] + 1
                risk[size * t + r, c] = nr if nr < 10 else 1
        for u in range(1, 5):
            for r, c in itertools.product(range(size), range(size)):
                nr = risk[size * t + r, size * (u - 1) + c] + 1
                risk[size * t + r, size * u + c] = nr if nr < 10 else 1

    size = size * 5
    return part1(risk, size)


with open("input-15.txt", "r") as f:
    risk = None
    for line in [l.strip() for l in f]:
        if risk is None:
            size = len(line)
            risk = numpy.zeros((size, size), numpy.int32)
            row = 0

        risk[row] = [int(c) for c in line]
        row += 1

    print("Part 1:", part1(risk, size))
    print("Part 2:", part2(risk, size))
