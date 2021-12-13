import io
import os
import time

input_data = open("input.txt", "r").readlines()


def pprint(data):
    for line in data:
        print("".join([(('*' if c == 0 else str(c)) if c < 10 else '-') for c in line]))
    print("")


def flash(data, y, x, ymax, xmax):
    if x > 0:
        data[y][x - 1] += 1
        if data[y][x - 1] == 10:
            flash(data, y, x - 1, ymax, xmax)
        if y > 0:
            data[y - 1][x - 1] += 1
            if data[y - 1][x - 1] == 10:
                flash(data, y - 1, x - 1, ymax, xmax)
        if y < ymax - 1:
            data[y + 1][x - 1] += 1
            if data[y + + 1][x - 1] == 10:
                flash(data, y + 1, x - 1, ymax, xmax)
    if x < xmax - 1:
        data[y][x + 1] += 1
        if data[y][x + 1] == 10:
            flash(data, y, x + 1, ymax, xmax)
        if y > 0:
            data[y - 1][x + 1] += 1
            if data[y - 1][x + 1] == 10:
                flash(data, y - 1, x + 1, ymax, xmax)
        if y < ymax - 1:
            data[y + 1][x + 1] += 1
            if data[y + 1][x + 1] == 10:
                flash(data, y + 1, x + 1, ymax, xmax)
    if y > 0:
        data[y - 1][x] += 1
        if data[y - 1][x] == 10:
            flash(data, y - 1, x, ymax, xmax)
    if y < ymax - 1:
        data[y + 1][x] += 1
        if data[y + 1][x] == 10:
            flash(data, y + 1, x, ymax, xmax)


def step(data):
    fcount = 0
    for y, line in enumerate(data):
        for x, value in enumerate(line):
            data[y][x] += 1
            if data[y][x] == 10:
                flash(data, y, x, len(data), len(line))

    for y, line in enumerate(data):
        for x, value in enumerate(line):
            if data[y][x] > 9:
                data[y][x] = 0
                fcount += 1

    return fcount

def all_zeros(data):
    for y, line in enumerate(data):
        for x, value in enumerate(line):
            if value != 0:
                return False
    return True

d = [[int(c) for c in line if c != "\n"] for line in input_data if line != "\n"]
flash_count = 0
for i in range(100):
    # pprint(d)
    flash_count += step(d)

# pprint(d)
print(flash_count)


d = [[int(c) for c in line if c != "\n"] for line in input_data if line != "\n"]
i = 0
while True:
    step(d)
    i += 1
    pprint(d)
    if all_zeros(d):
        break

print(i)