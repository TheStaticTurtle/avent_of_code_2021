import io
import os
import sys
import time

input_data = open("input.txt", "r").readlines()

polymer_template = input_data[0].replace("\n", "")

pairs = {x[0]: x[1] for x in [k.replace("\n", "").split(" -> ") for k in input_data[2:]]}


def step(value):
    out = value[0]
    offset = 0

    for value_pairs in [value[x:x + 2] for x in range(0, len(value), 1)]:
        if value_pairs in pairs.keys():
            out += pairs[value_pairs] + value_pairs[1]
        else:
            if len(value_pairs)==2:
               out += value_pairs

    return out


polymer = polymer_template
estimated_len = 0
for i in range(10):
    polymer = step(polymer)
    print(f"Step {i+1} {polymer}")
    # print(f"Step {i+1} lenght:{len(polymer)}")

print(f"Stats:")
out = {}
for c in polymer:
    if c not in out.keys():
        out[c] = polymer.count(c)

for key, value in out.items():
    print(f"{key} = {value}")

most = max(out.values())
least = min(out.values())

print(f"Most - Least: {most-least}")
