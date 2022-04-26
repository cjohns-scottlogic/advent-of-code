class Board:
    def __init__(self, boarddef):
        self.board = []
        self.done = False
        for row in boarddef:
            values = [(v, False) for v in row.split()]
            self.board.append(values)

    def reset(self):
        for row in range(0, 5):
            for column in range(0, 5):
                n = self.board[row][column][0]
                self.board[row][column] = (n, False)

    def call(self, n):
        if self.done:
            return False
        for row in range(0, 5):
            for column in range(0, 5):
                if self.board[row][column][0] == n:
                    self.board[row][column] = (n, True)
                    bingo = all(map(lambda x: x[1], self.board[row]))
                    if not bingo:
                        colvals = [row[column] for row in self.board]
                        bingo = all(map(lambda x: x[1], colvals))
                    if bingo:
                        self.done = True
                        return True
        return False

    def score(self, n):
        s = 0
        for row in range(0, 5):
            for column in range(0, 5):
                v = self.board[row][column]
                if v[1] == False:
                    s += int(v[0])
        return s * n


with open("input-04.txt", "r") as f:
    numbers = f.readline().strip().split(",")
    boards = []

    board = None
    for line in f:
        line = line.strip()
        if len(line) == 0:
            if board:
                boards.append(Board(board))
            board = []
        else:
            board.append(line)
    boards.append(Board(board))

    scores = []
    for n in numbers:
        for board in boards:
            if board.call(n):
                scores.append(board.score(int(n)))

    print("Part 1:", scores[0])
    print("Part 2:", scores[-1])
