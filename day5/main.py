import sys
from typing import IO

file = open("input.txt")

class Line:
    def __init__(self):
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

    def __repr__(self):
        return f"{self.x1},{self.y1} -> {self.x2},{self.y2}"

    def read(self, io:IO):
        l = io.readline()
        if l == "":
            return False
        a, b = [x.split(",") for x in l.split(" -> ")]
        self.x1, self.y1 = int(a[0]), int(a[1])
        self.x2, self.y2 = int(b[0]), int(b[1])
        print(self)
        return True


class Diag:
    def __init__(self):
        self.board = [[0 for _ in range(5)] for __ in range(5)]

    def __repr__(self):
        o = ""
        for y in self.board:
            o+=''.join([("." if x == 0 else str(x)) for x in y])
            o+="\n"
        return o

    def count(self, over):
        cnt = 0
        for y in self.board:
            for x in y:
                if x >= over:
                    cnt += 1
        return cnt

    def draw(self, line: Line):
        while line.y1 >= len(self.board) or line.y2 >= len(self.board):
            self.board.append([0 for _ in self.board[0]])

        while line.x1 >= len(self.board[0]) or line.x2 >= len(self.board[0]):
            for y in self.board:
                y.append(0)

        if line.y1 == line.y2:
            st = 1 if line.x2 >= line.x1 else -1
            for x in range(line.x1, line.x2+st, st):
                self.board[line.y1][x] += 1
        elif line.x1 == line.x2:
            st = 1 if line.y2 >= line.y1 else -1
            for y in range(line.y1, line.y2+st, st):
                self.board[y][line.x1] += 1
        else:
            stx = 1 if line.x2 >= line.x1 else -1
            y = line.y1
            for x in range(line.x1, line.x2+stx, stx):
                sty = 1 if line.y2 > line.y1 else -1
                if (sty == 1 and y < line.y2+sty) or (sty == -1 and y <= line.y1):
                    self.board[y][x] += 1
                y += sty
            print("qwerty")



lines = []
while True:
    l = Line()
    if not l.read(file):
        break
    # if l.x1 == l.x2 or l.y1 == l.y2:
    lines.append(l)

d = Diag()
for line in lines:
    d.draw(line)

print(d)
print(d.count(2))
