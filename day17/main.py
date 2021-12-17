import enum
import io
import multiprocessing
import os
import time
from dataclasses import dataclass
from typing import List

input_data = open("input.txt", "r").read().replace("\n", "")


class Probe:
    def __init__(self, x, y):
        self._initial_x = x
        self._initial_y = y
        self.initial_velocity_x = 0
        self.initial_velocity_y = 0
        self._velocity_x = 0
        self._velocity_y = 0
        self._x = x
        self._y = y
        self._fuel = None
        self._target = None
        self.apogee = float("-inf")

    @property
    def coordinates(self):
        return self._x, self._y

    def set_velocity(self, vx, vy):
        self.initial_velocity_x = vx
        self.initial_velocity_y = vy
        self._velocity_x = vx
        self._velocity_y = vy

    def tick(self):
        self._x += self._velocity_x
        self._y += self._velocity_y
        if self._velocity_x > 0:
            self._velocity_x -= 1
        if self._velocity_x < 0:
            self._velocity_x += 1

        self._velocity_y -= 1
        if self._fuel is not None:
            self._fuel -= 1

        if self._y > self.apogee:
            self.apogee = self._y

    def set_target(self, xmin, xmax, ymin, ymax):
        self._target = [xmin, xmax, ymin, ymax]

    def target_reached(self):
        if self._target is None:
            return False
        else:
            return self._target[0] <= self._x <= self._target[1] and self._target[2] <= self._y <= self._target[3]

    def could_reach_target(self):
        if self._target is None:
            return True
        else:
            return not (self._x > self._target[1] or self._y < self._target[2])

    def set_fuel(self, fuel):
        self._fuel = fuel

    def has_fuel(self):
        if self._fuel is None:
            return True
        else:
            return self._fuel > 0


class DynamicMap:
    FILL_CHAR = "."

    def __init__(self):
        self.board = [[self.FILL_CHAR for _ in range(5)] for __ in range(5)]
        self.zero_point = [0, 0]

    def _extend_map_to_point(self, x, y):
        _y = y + self.zero_point[0]
        _x = x + self.zero_point[1]

        if _y < 0:
            while abs(y) - 1 >= self.zero_point[0]:
                self.board.insert(0, [self.FILL_CHAR for _ in self.board[0]])
                self.zero_point[0] += 1
        else:
            while _y >= len(self.board):
                self.board.append([self.FILL_CHAR for _ in self.board[0]])

        if _x < 0:
            while abs(x) - 1 >= self.zero_point[1]:
                self.zero_point[1] += 1
                for yt in self.board:
                    yt.insert(0, self.FILL_CHAR)
        else:
            while _x >= len(self.board[0]):
                for yt in self.board:
                    yt.append(self.FILL_CHAR)

    def __repr__(self):
        o = ""
        for y in self.board:
            o += ''.join(y)
            o += "\n"
        return o

    def add_point(self, x, y, c):
        y *= -1
        self._extend_map_to_point(x, y)

        _y = y + self.zero_point[0]
        _x = x + self.zero_point[1]

        self.board[_y][_x] = c


MARKER_PROBE_INITIAL = "S"
MARKER_PROBE_PATH = "#"
MARKER_PROBE_TARGET = "T"

target_x_range, target_y_range = input_data.replace("target area: x=", "").replace(" y=", "").split(",")
target_x_range_min, target_x_range_max = [int(c) for c in target_x_range.split("..")]
target_y_range_min, target_y_range_max = [int(c) for c in target_y_range.split("..")]

def try_velocity(vx, vy):
    probe = Probe(0, 0)
    probe.set_target(target_x_range_min, target_x_range_max, target_y_range_min, target_y_range_max)
    probe.set_velocity(vx, vy)

    while probe.has_fuel() and not probe.target_reached() and probe.could_reach_target():
        probe.tick()

    return probe


PROCESSES = 10


def work(x_velocity_queue: multiprocessing.Queue, result_queue: multiprocessing.Queue):
    while not x_velocity_queue.empty():
        vx = x_velocity_queue.get()
        print(vx)
        for vy in range(-200, 1000):
            r = try_velocity(vx, vy)
            if r.target_reached():
                result_queue.put(r)
    return True


if __name__ == '__main__':
    queue = multiprocessing.Queue()
    rx_queue = multiprocessing.Queue()
    for _vx in range(0, target_x_range_max*10):
        queue.put(_vx)

    processes = []
    for n in range(PROCESSES):
        p = multiprocessing.Process(target=work, args=(queue, rx_queue))
        processes.append(p)
        p.start()


    while not queue.empty():
        time.sleep(1)

    best = None

    results = []
    while not rx_queue.empty():
        result = rx_queue.get()
        results.append(result)
        if best is None:
            best = result
            print(f"Velocity: vx={best.initial_velocity_x} vy={best.initial_velocity_y} TCR={best.could_reach_target()} TR={best.target_reached()} Apogee={best.apogee}")
        else:
            if best.apogee < result.apogee:
                best = result
                print(f"Velocity: vx={result.initial_velocity_x} vy={result.initial_velocity_y} TCR={result.could_reach_target()} TR={result.target_reached()} Apogee={result.apogee}")

    map = DynamicMap()
    for y in range(target_y_range_min, target_y_range_max + 1):
        for x in range(target_x_range_min, target_x_range_max + 1):
            map.add_point(x, y, MARKER_PROBE_TARGET)

    p = Probe(0, 0)
    p.set_target(target_x_range_min, target_x_range_max, target_y_range_min, target_y_range_max)
    p.set_velocity(best.initial_velocity_x, best.initial_velocity_y)

    while p.has_fuel() and not p.target_reached() and p.could_reach_target():
        p.tick()
        map.add_point(*p.coordinates, MARKER_PROBE_PATH)

    print()
    print()
    print(map)
    print()
    print(f"Velocity: vx={best.initial_velocity_x} vy={best.initial_velocity_y} TCR={best.could_reach_target()} TR={best.target_reached()} Apogee={best.apogee}")

    print(len(results))

