import sys
from typing import IO

file = open("input.txt")
raw = file.readline()

numbers = [int(x) for x in raw.split(",")]

print(f"Numbers {numbers}")

class Board:
    def __init__(self):
        self.grid = None
        self.marked = [[False for _ in range(5)] for __ in range(5)]

    def read(self, io: IO):
        io.readline()  # skip empty line
        lines = [io.readline() for _ in range(5)]
        self.grid = [[int(num) for num in line.split(" ") if num] for line in lines]
        if len(self.grid[0]) == 0:  # Read failed
            return False
        # print(self, self.grid)
        return True

    def mark(self, number):
        for y in range(5):
            for x in range(5):
                if self.grid[y][x] == number:
                    self.marked[y][x] = True
                    # print(self, y, x, number, self.grid[y][x], self.marked)

    def has_won(self):
        won = None
        for line in self.marked:
            if line.count(False) == 0:
                won = True

        for y in range(5):
            k = [i[y] for i in self.marked]
            if k.count(False) == 0:
                won = True

        if won:
            s = 0
            for y in range(5):
                for x in range(5):
                    if self.marked[y][x]:
                        self.grid[y][x] =0
                s += sum(self.grid[y])

            return s
        return won




boards = []
while True:
    b = Board()
    if not b.read(file):
        break
    boards.append(b)

last = None, None, None
done = []

for number in numbers:
    for board in boards:
        if board not in done:
            board.mark(number)
            state = board.has_won()
            if state is not None:
                done.append(board)
                last = board, number, state

board, number, state = last
print("END: ", state * number)

