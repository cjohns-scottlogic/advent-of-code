class Enhancer:
    def __init__(self, data):
        self.data = data
        assert len(self.data) == 512

    def __call__(self, image):
        min_x, min_y, max_x, max_y = image.limits()

        for x in range(min_x - 2, max_x + 3):
            for y in range(min_y - 2, max_y + 3):
                image.update(x, y, self.enhanced(image, x, y))

        image.apply()
        image.bg = self.data[0b000000000 if image.bg == "." else 0b111111111]

    def enhanced(self, image, x, y):
        return self.data[image.value(x, y)]


class Image:
    def __init__(self, data):
        self.pixels = {}
        self.updates = []
        self.bg = "."
        if data is not None:
            y = 0
            for line in data:
                x = 0
                for c in line:
                    self.pixels[(x, y)] = c
                    x += 1
                y += 1

    def clone(self):
        c = Image(None)
        for z in self.pixels.keys():
            c.pixels[z] = self.pixels[z]
        return c

    def pixel(self, x, y):
        if (x, y) not in self.pixels:
            return self.bg
        return self.pixels[(x, y)]

    def set(self, x, y, new):
        self.pixels[(x, y)] = new

    def update(self, x, y, new):
        self.updates.append((x, y, new))

    def apply(self):
        for x, y, new in self.updates:
            self.pixels[x, y] = new
        self.updates = []

    def limits(self):
        min_x = min_y = max_x = max_y = 0
        for x, y in self.pixels.keys():
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, x)

        return min_x, min_y, max_x, max_y

    def print(self):
        min_x, min_y, max_x, max_y = self.limits()
        for y in range(min_y, max_y + 1):
            line = ""
            for x in range(min_x, max_x + 1):
                if (x, y) in self.pixels:
                    line += self.pixels[(x, y)]
                else:
                    line += "."
            print(line)

    def value(self, x, y):
        pixels = ""
        for y1 in range(y - 1, y + 2):
            for x1 in range(x - 1, x + 2):
                pixels += self.pixel(x1, y1)
        return int(pixels.replace(".", "0").replace("#", "1"), 2)

    def count(self):
        return list(self.pixels.values()).count("#")


with open("input-20.txt", "r") as f:
    enhancer = Enhancer(f.readline().strip())
    f.readline()
    image = []
    for line in f:
        line = line.strip()
        image.append(line)
    image = Image(image)

for x in range(0, 50):
    if x == 2:
        print("Part 1:", image.count())
    enhancer(image)

print("Part 2:", image.count())
