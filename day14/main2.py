import io
import os
import sys
import time
from collections import defaultdict

input_data = open("input.txt", "r").readlines()

polymer_template = input_data[0].replace("\n", "")

pairs = {x[0]: x[1] for x in [k.replace("\n", "").split(" -> ") for k in input_data[2:]]}

# Frequency table, this will hold the number of time a pair appears
frequencies = defaultdict(int)

# Save every pair of letters in the a frequency table
for i in range(len(polymer_template) - 1):
    pair = polymer_template[i: i + 2]
    frequencies[pair] += 1

print(frequencies)

for i in range(40):
    new_frequencies = defaultdict(int)
    for pair, freq in frequencies.items():
        # Find the coresponding pair and add the frequency
        new_frequencies[f"{pair[0]}{pairs[pair]}"] += freq
        new_frequencies[f"{pairs[pair]}{pair[1]}"] += freq
        frequencies = new_frequencies
        print(frequencies)

letter_frequencies = defaultdict(int)
for pair in frequencies:
    # Count the number of time a letter appears first in the frequencies
    letter_frequencies[pair[0]] += frequencies[pair]

# Dont forget the last one or the answer won't be valid
letter_frequencies[polymer_template[-1]] += 1

#Find the min/max
max_letter = max(letter_frequencies.items(), key=lambda x: x[1])
min_letter = min(letter_frequencies.items(), key=lambda x: x[1])

print(letter_frequencies)
print(max_letter)
print(min_letter)
print(max_letter[1] - min_letter[1])