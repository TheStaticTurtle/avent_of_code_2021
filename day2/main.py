
input_data = [c.split(" ") for c in open("input.txt", "r").read().split("\n") if c]

horizontal = 0
depth = 0

for command, raw_delta in input_data:
    delta = int(raw_delta)
    if command == "forward":
        horizontal += delta
    if command == "up":
        depth -= delta
    if command == "down":
        depth += delta

print(f"Part one:   Horizontal: {horizontal} Depth: {depth} Answer: {horizontal*depth}")

horizontal = 0
depth = 0
aim = 0

for command, raw_delta in input_data:
    delta = int(raw_delta)
    if command == "forward":
        horizontal += delta
        depth += aim * delta
    if command == "up":
        aim -= delta
    if command == "down":
        aim += delta

print(f"Part two:   Horizontal: {horizontal} Depth: {depth} Answer: {horizontal*depth}")