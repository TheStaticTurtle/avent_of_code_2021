import io
import os
import time

input_data = open("input.txt", "r").readlines()

class Sheet:
    def __init__(self):
        self.board = [[" " for _ in range(5)] for __ in range(5)]

    def __repr__(self):
        o = ""
        for y in self.board:
            o += ''.join(y)
            o += "\n"
        return o

    def add_point(self, x, y):
        while y >= len(self.board):
            self.board.append([" " for _ in self.board[0]])

        while x >= len(self.board[0]):
            for yt in self.board:
                yt.append(" ")

        # print(x,y)
        self.board[y][x] = "#"

    def points(self):
        c = 0
        for y, line in enumerate(self.board):
            for x, v in enumerate(line):
                if v == "#":
                    c += 1
        return c



    def fold_y(self, at):
        upper_half = self.board[:at]
        lower_half = self.board[at+1:]

        for iy, line in enumerate(lower_half):
            for x, vx in enumerate(line):
                if vx == "#":
                    upper_half[len(upper_half) - 1 - iy][x] = "#"
        # print(upper_half)
        # print(lower_half)
        self.board = upper_half

    def fold_x(self, at):
        out = []
        for line in self.board:
            left = line[:at]
            right = line[at+1:]

            for x, xv in enumerate(right):
                if xv == "#":
                    left[len(left)-1-x] = "#"

            out.append(left)

        self.board = out



s = Sheet()

for line in input_data:
    if line.startswith("fold"):
        if "fold along y" in line:
            s.fold_y(int(line.split("y=")[1]))
        if "fold along x" in line:
            s.fold_x(int(line.split("x=")[1]))
        print(s.points())
    elif line=="\n":
        pass
    else:
        v = line.split(",")
        if len(v) == 2:
            s.add_point(int(v[0]), int(v[1]))

print(s)
