def part1(data):
    err = 0
    for line in data:
        stack = []
        for c in line:
            if c in "([{<":
                stack.append(c)
            else:
                last = stack.pop()
                match c:
                    case ")":
                        if last != "(":
                            err += 3
                            break
                    case "]":
                        if last != "[":
                            err += 57
                            break
                    case "}":
                        if last != "{":
                            err += 1197
                            break
                    case ">":
                        if last != "<":
                            err += 25137
                            break

    return err


def part2(data):
    scores = []
    for line in data:
        stack = []
        error = False
        for c in line:
            if c in "([{<":
                stack.append(c)
            else:
                last = stack.pop()
                match c:
                    case ")":
                        if last != "(":
                            error = True
                    case "]":
                        if last != "[":
                            error = True
                    case "}":
                        if last != "{":
                            error = True
                    case ">":
                        if last != "<":
                            error = True
        if not error:
            score = 0
            for c in reversed(stack):
                score = score * 5 + ("([{<}]".index(c) + 1)
            scores.append(score)

    mid = (len(scores) + 1) // 2
    return sorted(scores)[mid - 1]


with open("input-10.txt", "r") as f:
    data = [line.strip() for line in f]

    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
