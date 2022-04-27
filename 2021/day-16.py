from math import prod


class BitStream:
    def __init__(self, hex_data):
        self.hex_data = hex_data
        self.ptr = 0

    def __call__(self, n):
        v = 0
        first = (self.ptr) // 4
        last = (self.ptr + n + 3) // 4

        v = int(self.hex_data[first:last], 16)
        q = self.ptr + n
        if q % 4:
            v = v >> (4 - (q % 4))

        v = v & ((1 << n) - 1)

        self.ptr += n
        return v


def process_packet(bits):
    vsum = 0
    version = bits(3)
    type_id = bits(3)

    vsum += version

    if type_id == 4:
        v = 0
        part = 0x10
        while part & 0x10:
            part = bits(5)
            v = (v * 16) + (part & 0xF)
        return v, vsum

    else:
        v = []
        len_type = bits(1)
        if len_type == 0:
            sub_size = bits(15)
            start = bits.ptr
            while bits.ptr < start + sub_size:
                va, vs = process_packet(bits)
                v.append(va)
                vsum += vs

        if len_type == 1:
            sub_count = bits(11)
            for _ in range(sub_count):
                va, vs = process_packet(bits)
                v.append(va)
                vsum += vs

    rv = 0
    match type_id:
        case 0:
            rv = sum(v)
        case 1:
            rv = prod(v)
        case 2:
            rv = min(v)
        case 3:
            rv = max(v)
        case 5:
            rv = 1 if v[0] > v[1] else 0
        case 6:
            rv = 1 if v[0] < v[1] else 0
        case 7:
            rv = 1 if v[0] == v[1] else 0

    return rv, vsum


with open("input-16.txt", "r") as f:
    data = f.read().strip()
    bits = BitStream(data)

    part2, part1 = process_packet(bits)

    print("Part 1:", part1)
    print("Part 2:", part2)
