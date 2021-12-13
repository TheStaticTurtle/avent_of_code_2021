import io
import os
import time

input_data = open("input.txt", "r").readlines()

class Cave:
    system = {}

    def __new__(cls, name: str):
        if name in cls.system:
            return cls.system[name]  # Return the existing instance
        else:
            self = super().__new__(cls)
            cls.system[name] = self  # Create a new instance

            self.name = name
            self.is_start = name == "start"
            self.is_end = name == "end"
            self.is_big = name.isupper()
            self.is_small = not self.is_big

            self.tunnels = set()
            return self

    def dig_tunnel(self, other_cave) -> None:
        self.tunnels.add(other_cave)
        other_cave.tunnels.add(self)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"{self.name}"



for line in input_data:
    a, b = [w.replace("\n","") for w in line.split("-")]

    ca = Cave(a)
    cb = Cave(b)
    ca.dig_tunnel(cb)


def find_path(caves, extra_visit=False):
    paths = []

    def travel(position, has_extra_visit, route=[]):
        if position == Cave("start") and len(route) > 1:
            return

        if position == Cave("end"):
            paths.append(route + [position])
            return

        if position.is_small:
            max_visits = 2 if has_extra_visit else 1
            visit_count = route.count(position) + 1
            if visit_count == max_visits:
                has_extra_visit = False
            if visit_count > max_visits:
                return

        # Try each possible exit
        for next_cave in position.tunnels:
            travel(next_cave, has_extra_visit, route + [position])

    # Begin recursive search of all paths
    travel(caves["start"], extra_visit, [])
    return paths


routes_p1 = find_path(Cave.system, False)
print(f"Part 1: {len(routes_p1)}")

routes_p2 = find_path(Cave.system, True)
print(f"Part 2: {len(routes_p2)}")

print(Cave("start").tunnels)