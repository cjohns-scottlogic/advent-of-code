import functools
import itertools
from collections import deque


def mapbit(x, y):
    if y == 0:
        return [0, 1, None, 2, None, 3, None, 4, None, 5, 6][x]
    col = [None, None, 0, None, 1, None, 2, None, 3, None, None][x]
    return None if col is None else 11 + ((y - 1) * 4) + col


def move_cost(type):
    return {"A": 1, "B": 10, "C": 100, "D": 1000}[type]


def target_room(type):
    return {"A": 2, "B": 4, "C": 6, "D": 8}[type]


class State:
    def __init__(self, energy, depth, locations):
        self.energy = energy
        self.depth = depth
        self.locations = locations
        self._hash = None

    def __repr__(self):
        return "energy:{} Locations {}".format(self.energy, self.locations)

    def __hash__(self):
        if self._hash is None:
            self._hash = 0
            maplocs = {}
            for (x, y), (type, home) in self.locations.items():
                maplocs[mapbit(x, y)] = ord(type) - ord("A")

            offset = 32
            for i in sorted(maplocs.keys()):
                self._hash |= 1 << i
                self._hash |= maplocs[i] << offset
                offset += 2

        return self._hash

    @property
    def home(self):
        return functools.reduce(
            lambda a, b: a + b, map(lambda a: a[1], self.locations.values())
        )

    @property
    def cost(self):
        return (
            self.energy if all(map(lambda a: a[1], self.locations.values())) else None
        )


# Returns the best target for the given amphipod, regardless of if it can get there
def get_target(state, type):
    x = target_room(type)

    for y in range(state.depth, 0, -1):
        t = state.locations.get((x, y))
        if t is None or t[0] != type:
            return (x, y)

    raise RuntimeError("Can't find target for {}".format(type))


# Returns the path cost to move from 'frm' to 'to', or None if it's blocked
def path_cost(state, frm, to):
    loc = frm
    cost = 0

    while loc[1] != 0 and cost is not None:
        loc = (loc[0], loc[1] - 1)
        cost = (cost + 1) if loc not in state.locations.keys() else None

    while loc[0] != to[0] and cost is not None:
        loc = (loc[0] + (1 if to[0] > loc[0] else -1), 0)
        cost = (cost + 1) if loc not in state.locations.keys() else None

    while loc[1] != to[1] and cost is not None:
        loc = (loc[0], loc[1] + 1)
        cost = (cost + 1) if loc not in state.locations.keys() else None

    return cost


def next_states(state):
    states = []

    for (x, y), (type, home) in state.locations.items():
        if home:
            continue

        # Where do we want to get to?
        target = get_target(state, type)

        # Can we move directly to the target?
        cost = path_cost(state, (x, y), target)
        if cost is not None:
            new_locs = dict(filter(lambda a: a[0] != (x, y), state.locations.items()))
            new_locs[target] = (type, True)
            states.append(
                State(state.energy + cost * move_cost(type), state.depth, new_locs)
            )

        # No, so if we're not in the corridor see if we can move there.
        elif y != 0:
            for x1 in [0, 1, 3, 5, 7, 9, 10]:
                cost = path_cost(state, (x, y), (x1, 0))
                if cost is not None:
                    new_locs = dict(
                        filter(lambda a: a[0] != (x, y), state.locations.items())
                    )
                    new_locs[(x1, 0)] = (type, False)
                    states.append(
                        State(
                            state.energy + cost * move_cost(type), state.depth, new_locs
                        )
                    )
    return states


def get_data(puzzle):
    return list(
        map(
            lambda s: s.split(),
            filter(
                len,
                [
                    line.translate(str.maketrans("#.", "  ")).strip()
                    for line in puzzle.splitlines()
                ],
            ),
        )
    )


def solve(data):
    locations = {}
    depth = len(data)
    verbose = False
    cheapest = None

    for l, a in itertools.product(range(depth), range(4)):
        locations[((a + 1) * 2, l + 1)] = (data[l][a], False)

    states = deque([State(0, depth, locations)])

    if verbose:
        last_printed = None

    while len(states) > 0:
        if verbose:
            cstates = len(states) // 100
            if cstates != last_printed:
                print(
                    "Queue: {}K states, cheapest: {}   \r".format(
                        cstates / 10, cheapest
                    ),
                    end="",
                    flush=True,
                )
                last_printed = cstates

        for state in next_states(states.popleft()):
            if state.cost is not None:
                if cheapest is None or state.cost < cheapest:
                    cheapest = state.cost
            else:
                add = True
                for s1 in states:
                    if hash(s1) == hash(state):
                        add = False
                        s1.energy = min(s1.energy, state.energy)

                if add:
                    states.append(state)

    if verbose:
        print("")

    return cheapest


puzzle_1 = """
#############
#...........#
###D#B#D#B###
  #C#A#A#C#
  #########
"""

puzzle_2 = """
#############
#...........#
###D#B#D#B###
  #D#C#B#A#
  #D#B#A#C#
  #C#A#A#C#
  #########
"""

part_1 = solve(get_data(puzzle_1))
part_2 = solve(get_data(puzzle_2))

print("Part 1:", part_1)
print("Part 2:", part_2)
