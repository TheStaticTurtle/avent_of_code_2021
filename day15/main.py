import io
import os
import time
from dataclasses import dataclass
from typing import List

input_data = open("input.txt", "r").read().splitlines()


@dataclass
class Point:
    y: int
    x: int
    risk: int

    def __repr__(self):
        return str(self.risk)


risk_table = [
    [Point(y, x, int(c)) for x, c in enumerate(line)]
    for y, line in enumerate(input_data)
]
height = len(risk_table)
width = len(risk_table[0])

expand_times = 5

all_tiles = [
    [None] * (width * expand_times) for _ in range(height * expand_times)
]

for y in range(height * expand_times):
    for x in range(width * expand_times):
        old = risk_table[y % height][x % width]
        offset = y // height + x // width

        risk = (old.risk + offset - 1) % 9 + 1
        all_tiles[y][x] = Point(y, x, risk)

risk_table = all_tiles
height *= expand_times
width *= expand_times


def neighbors(point: Point) -> List[Point]:
    neighbors = []
    if point.y > 0:
        neighbors.append(risk_table[point.y - 1][point.x])
    if point.y < height - 1:
        neighbors.append(risk_table[point.y + 1][point.x])
    if point.x > 0:
        neighbors.append(risk_table[point.y][point.x - 1])
    if point.x < width - 1:
        neighbors.append(risk_table[point.y][point.x + 1])
    return neighbors


cost = [[float("inf") for x in range(width)] for y in range(height)]

start = risk_table[0][0]
end = risk_table[-1][-1]
cost[start.y][start.x] = 0

queue = [start]
while queue:
    current = queue.pop(0)
    nn = neighbors(current)
    for n in nn:
        if cost[n.y][n.x] > cost[current.y][current.x] + n.risk:
            cost[n.y][n.x] = cost[current.y][current.x] + n.risk
            queue.append(n)


# for l in risk_table:
#     print(l)
# print()
# print()
# print()
# for l in cost:
#     print(l)
print(cost[end.y][end.x])
