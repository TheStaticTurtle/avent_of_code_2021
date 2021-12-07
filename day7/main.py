import math
import statistics

file = open("input.txt")

crabs = [int(x) for x in file.readline().split(",")]
crabs_fuel = [0] * len(crabs)

print(f"Mean: {statistics.mean(crabs)}")
print(f"Median: {statistics.median(crabs)}")


def do(target):
    def craby(pos_offset: int) -> int:
        fuel = 0
        counter = 1
        for i in range(pos_offset):
            fuel += counter
            counter += 1
        return fuel

    for c_i in range(len(crabs)):
        offset = crabs[c_i] - target
        crabs_fuel[c_i] = craby(abs(offset))

    return sum(crabs_fuel)


# print(do(math.ceil(statistics.mean(crabs))))

# Bruteforce don't care
m = 9999999999999999999
for i in range(0, max(crabs)):
    n = do(i)
    if n < m:
        print(n)
        m = n
print(m)
