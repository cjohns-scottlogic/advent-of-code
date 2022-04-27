input = "target area: x=155..182, y=-117..-67"


class XY:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def __repr__(self):
        return "(x={} y={})".format(self.x, self.y)


class Box:
    def __init__(self):
        self.min = XY()
        self.max = XY()

    def __repr__(self):
        return "({},{} - {},{})".format(self.min.x, self.min.y, self.max.x, self.max.y)

    def hit(self, xy):
        return self.min.x <= xy.x <= self.max.x and self.max.y >= xy.y >= self.min.y


target = Box()

for i in [i.strip() for i in input.split(": ")[1].split(",")]:
    mn, mx = i[2:].split("..")
    if i.startswith("x="):
        target.min.x, target.max.x = int(mn), int(mx)
    elif i.startswith("y="):
        target.min.y, target.max.y = int(mn), int(mx)

highest = 0
hits = []

for y in range(target.min.y - 1, -target.min.y + 1):
    for x in range(0, target.max.x + 1):
        pos = XY(0, 0)
        velocity = XY(x, y)
        high = 0

        while pos.x <= target.max.x and pos.y >= target.min.y:
            pos.x += velocity.x
            pos.y += velocity.y
            high = max(high, pos.y)

            if target.hit(pos):
                highest = max(highest, high)
                if (x, y) not in hits:
                    hits.append((x, y))

            if velocity.x > 0:
                velocity.x -= 1
            elif velocity.x < 0:
                velocity.x += 1

            velocity.y -= 1

print("Part 1:", highest)
print("Part 2:", len(hits))
