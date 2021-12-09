import functools
import math
import statistics

from typing import List


class Basin:
    __slots__ = 'origin', 'points'

    def __init__(self, minima):
        self.origin = minima

        self.points = [self.origin]

        continue_loop = True
        while continue_loop:
            point_append = []
            for cell in self.points:
                top, bottom, left, right = cell.top, cell.bottom, cell.left, cell.right
                if top and top not in self.points and top not in point_append and top.h > cell.h and top.h != 9:
                    point_append.append(top)
                if bottom and bottom not in self.points and bottom not in point_append and bottom.h > cell.h and bottom.h != 9:
                    point_append.append(bottom)
                if left and left not in self.points and left not in point_append and left.h > cell.h and left.h != 9:
                    point_append.append(left)
                if right and right not in self.points and right not in point_append and right.h > cell.h and right.h != 9:
                    point_append.append(right)
            self.points += point_append
            # print(point_append)
            if len(point_append) == 0:
                continue_loop = False

        # print(self.points)

    @property
    @functools.lru_cache()
    def size(self):
        return len(self.points)

    def __repr__(self):
        return f"<Basin origin={self.origin} size={self.size}>"


class Point:
    __slots__ = 'map', 'x', 'y', 'h'

    def __init__(self, map, x, y):
        self.map = map
        self.x = x
        self.y = y
        self.h = self.map[y][x]

    def __repr__(self):
        return f"<Minima x={self.x} y={self.y} height={self.h}>"

    def __eq__(self, value):
        return self.x == value.x and self.y == value.y and self.h == value.h

    @property
    def top(self):
        if self.y - 1 >= 0:
            return Point(self.map, self.x, self.y - 1)

    @property
    def bottom(self):
        if self.y + 1 < len(self.map):
            return Point(self.map, self.x, self.y + 1)

    @property
    def left(self):
        if self.x - 1 >= 0:
            return Point(self.map, self.x - 1, self.y)

    @property
    def right(self):
        if self.x + 1 < len(self.map[self.y]):
            return Point(self.map, self.x + 1, self.y)

    def get_basin(self) -> Basin:
        return Basin(self)


def minima_finder(inp) -> List[Point]:
    output = []
    for y, row in enumerate(inp):
        for x, height in enumerate(row):
            minima = True
            if x - 1 >= 0 and height >= row[x - 1]:
                minima = False
            if x + 1 < len(row) and height >= row[x + 1]:
                minima = False
            if y - 1 >= 0 and height >= inp[y - 1][x]:
                minima = False
            if y + 1 < len(inp) and height >= inp[y + 1][x]:
                minima = False

            if minima:
                output.append(Point(inp, x, y))

    return output


file = open("input.txt")
data_input = [[int(c) for c in x] for x in file.read().splitlines()]

minimas = minima_finder(data_input)

risk = sum([minima.h for minima in minimas]) + len(minimas)
print(f"Risk (part1): {risk}")

bassins = [minima.get_basin() for minima in minimas]

bassins.sort(key=lambda x: x.size, reverse=True)

size = 1
for bassin in bassins[:3]:
    print(bassin)
    size *= bassin.size

risk = sum([minima.h for minima in minimas])
print(f"3 biggest bassins: {size}")