
input_data = [c for c in open("input.txt", "r").read().split("\n") if c]

gamma_rate = ""
epsilon_rate = ""

columns = [''.join([c[i] for c in input_data]) for i in range(len(input_data[0]))]

for column in columns:
    if column.count("1") > column.count("0"):
        gamma_rate += "1"
        epsilon_rate += "0"
    else:
        gamma_rate += "0"
        epsilon_rate += "1"

gamma_rate = eval(f"0b{gamma_rate}")
epsilon_rate = eval(f"0b{epsilon_rate}")

print(f"Part one:   Gamma: {gamma_rate} Epsilon: {epsilon_rate} Answer: {gamma_rate*epsilon_rate}")


def search(data, search_oxygen=True):
    bit_i = 0
    while len(data) > 1:
        # print(data)
        column = [''.join([c[bit_i] for c in data])][0]
        keep = None
        if column.count("1") > column.count("0"):
            keep = "1" if search_oxygen else "0"
        elif column.count("0") == column.count("1"):
            keep = "1" if search_oxygen else "0"
        else:
            keep = "0" if search_oxygen else "1"
        data = [c for c in data if c[bit_i] == keep]
        bit_i+=1
    return data[0]


oxygen_rating = search(input_data, search_oxygen=True)
co2_rating = search(input_data, search_oxygen=False)

oxygen_rating = eval(f"0b{oxygen_rating}")
co2_rating = eval(f"0b{co2_rating}")

print(f"Part two:   Oxygen: {oxygen_rating} Co2: {co2_rating} Answer: {oxygen_rating*co2_rating}")
