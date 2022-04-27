import itertools


class SnailfishNumber:
    def __init__(self, s):
        if s.__class__ is str:
            assert s[0] == "["
            assert s[-1] == "]"

            l = ""
            r = ""
            t = s[1:-1]
            z = 0
            q = False
            for c in t:
                if c == "," and z == 0:
                    q = True
                    continue

                if c == "[":
                    z += 1
                if c == "]":
                    z -= 1
                if q:
                    r += c
                else:
                    l += c

            self.l = SnailfishNumber(l) if l[0] == "[" else int(l)
            self.r = SnailfishNumber(r) if r[0] == "[" else int(r)
        else:
            self.l = s[0]
            self.r = s[1]

    def __repr__(self):
        return "[{},{}]".format(self.l, self.r)

    def magnitude(self):
        lmag = 3 * (self.l if self.l.__class__ is int else self.l.magnitude())
        rmag = 2 * (self.r if self.r.__class__ is int else self.r.magnitude())
        return lmag + rmag


class ExplodingNumber:
    def __init__(self, l, r):
        self.l = l
        self.r = r
        self.replaced = False

    def __repr__(self):
        return "Exploding Number [{},{}] {}".format(self.l, self.r, self.replaced)


def find_explode(n, level=0):
    if level > 3:
        # print("Explode",n)
        return ExplodingNumber(n.l, n.r)

    if n.l.__class__ is SnailfishNumber:
        x = find_explode(n.l, level + 1)
        if x:
            # print(x, n,"l")
            if not x.replaced:
                n.l = 0
                x.replaced = True
                if n.r.__class__ is int:
                    n.r += x.r
                    x.r = 0
                else:
                    z = n.r
                    while z.l.__class__ != int:
                        z = z.l
                    z.l += x.r
                    x.r = 0
                return x
            else:
                if x.r > 0:
                    if n.r.__class__ is int:
                        n.r += x.r
                    else:
                        z = n.r
                        while z.l.__class__ != int:
                            z = z.l
                        z.l += x.r
                    x.r = 0
                return x

    if n.r.__class__ is SnailfishNumber:
        x = find_explode(n.r, level + 1)
        if x:
            # print(x, n,"r")
            if not x.replaced:
                n.r = 0
                x.replaced = True
                if n.l.__class__ == int:
                    n.l += x.l
                    x.l = 0
                else:
                    z = n.l
                    while z.r.__class__ != int:
                        z = z.r
                    z.r += x.l
                    x.l = 0
                return x
            else:
                if x.l > 0:
                    if n.l.__class__ is int:
                        n.l += x.l
                    else:
                        z = n.l
                        while z.r.__class__ != int:
                            z = z.r
                        z.r += x.l
                    x.l = 0
                return x


def find_split(n):
    if n.l.__class__ is int:
        if n.l >= 10:
            n.l = SnailfishNumber((n.l // 2, (n.l + 1) // 2))
            return True
    else:
        if find_split(n.l):
            return True

    if n.r.__class__ is int:
        if n.r >= 10:
            n.r = SnailfishNumber((n.r // 2, (n.r + 1) // 2))
            return True
    else:
        if find_split(n.r):
            return True

    return False


def add(a, b):
    n = SnailfishNumber((a, b))
    reducing = True
    while reducing:
        reducing = find_explode(n) or find_split(n)
    return n


with open("input-18.txt", "r") as f:
    values = [line.strip() for line in f.readlines()]

    sum = None
    for i in values:
        if sum is None:
            sum = SnailfishNumber(i)
        else:
            sum = add(sum, SnailfishNumber(i))

    print("Part 1:", sum.magnitude())

with open("input-18.txt", "r") as f:

    highest = 0
    for a, b in itertools.product(range(len(values)), range(len(values))):
        if a != b:
            sum = add(SnailfishNumber(values[a]), SnailfishNumber(values[b]))
            highest = max(highest, sum.magnitude())
            # print(a, b, sum.magnitude())

    print("Part 2:", highest)
