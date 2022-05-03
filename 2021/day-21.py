import itertools

input = [8, 9]


class Player:
    def __init__(self, start, score=0):
        self.pos = start
        self.score = score

    def advance(self, n):
        pos = self.pos + n
        while pos > 10:
            pos -= 10
        return Player(pos, self.score + pos)


class DeterminsticDie:
    def __init__(self, sides):
        self.sides = sides
        self.last = 0
        self.count = 0

    def roll(self):
        self.last = self.last + 1 if self.last < self.sides else 1
        self.count += 1
        return self.last


def part1(p1, p2):
    turn = 1

    d = DeterminsticDie(100)

    while p1.score < 1000 and p2.score < 1000:
        move = d.roll() + d.roll() + d.roll()
        if turn == 1:
            p1 = p1.advance(move)
            turn = 2
        else:
            p2 = p2.advance(move)
            turn = 1

    return min(p1.score, p2.score) * d.count


def part2(p1, p2):
    counts = {}
    for a, b, c in itertools.product(range(1, 4), range(1, 4), range(1, 4)):
        s = a + b + c
        if s not in counts:
            counts[s] = 1
        else:
            counts[s] += 1

    wins = {1: 0, 2: 0}

    p1_win = 0
    p2_win = 0

    def move(turn, p1, p2, u, wins):
        if p1.score >= 21:
            wins[1] += u
            return

        if p2.score >= 21:
            wins[2] += u
            return

        match turn:
            case 1:
                for v, c in counts.items():
                    p1n = p1.advance(v)
                    move(2, p1n, p2, u * c, wins)

            case 2:
                for v, c in counts.items():
                    p2n = p2.advance(v)
                    move(1, p1, p2n, u * c, wins)

    move(1, p1, p2, 1, wins)
    return max(wins.values())


player_1 = Player(input[0])
player_2 = Player(input[1])

print("Part 1:", part1(player_1, player_2))
print("Part 2:", part2(player_1, player_2))
