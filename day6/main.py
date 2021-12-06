import sys
from typing import IO

file = open("input.txt")

class Fish:
    def __init__(self, left, born=False):
        self.left = left
        if born:
            self.left += 2

    def __repr__(self):
        return str(self.left)

    @staticmethod
    def birth():
        return Fish(7, born=True)

    def cycle(self):
        if self.left == 0:
            self.left = 6
            return Fish.birth()
        else:
            self.left -= 1
        return None

fishs = [Fish(int(x)) for x in file.readline().split(",")]

print(f"Initial: {','.join([repr(f) for f in fishs])}")

for d in range(256):
    for fish in fishs:
        k = fish.cycle()
        if k:
            fishs.append(k)
    print(f"{d} -> {len(fishs)}")
    # print(f"Day {d+1}: {','.join([repr(f) for f in fishs])}")

print(f"Count: {len(fishs)}")


