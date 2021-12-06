import sys

file = open("input.txt")

fish_count = [0,0,0,0,0,0,0,0,0]

for x in file.readline().split(","):
    fish_count[int(x)] += 1


print(f"Initial: {fish_count}")

for d in range(256):
    newborns = fish_count[0]

    for i in range(8):
        fish_count[i] = fish_count[i+1]

    fish_count[8] = newborns
    fish_count[6] += newborns

    print(f"{d} -> {fish_count}")


print(f"{sum(fish_count)}")
