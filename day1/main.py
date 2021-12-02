
input_data = [int(i) for i in open("input.txt", "r").read().split("\n") if i]
print(input_data)

last = input_data[0]
counter = 0

for i in input_data[1:]:
    if i > last:
        counter += 1
    last = i

print(f"Part one: {counter}")

window_size = 3
input_windowed = []
for i in range(len(input_data)):
    input_windowed.append(sum(input_data[i:i+3]))

print(input_windowed)

last = input_windowed[0]
counter = 0

for i in input_windowed[1:]:
    if i > last:
        counter += 1
    last = i

print(f"Part two: {counter}")