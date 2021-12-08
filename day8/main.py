import math
import statistics

file = open("input.txt")

input = [str(x) for x in file.read().splitlines()]

# input = ["acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"]


segments_for_i = {
    0: {'a', 'e', 'g', 'c', 'f', 'b'},
    1: {'f', 'c'},
    2: {'a', 'e', 'g', 'd', 'c'},
    3: {'a', 'g', 'd', 'c', 'f'},
    4: {'d', 'f', 'c', 'b'},
    5: {'a', 'g', 'd', 'f', 'b'},
    6: {'a', 'e', 'g', 'd', 'f', 'b'},
    7: {'a', 'c', 'f'},
    8: {'a', 'e', 'g', 'd', 'c', 'f', 'b'},
    9: {'a', 'g', 'd', 'c', 'f', 'b'}
}


total = 0
total1478 = 0

for line in input:
    signals, outputs = line.split(" | ")
    signals = signals.split(" ")
    outputs = outputs.split(" ")
    translated = [None for _ in outputs]

    counts = {
        "1": [],
        # "2": [],
        # "3": [],
        "4": [],
        "5": [],
        "6": [],
        "7": [],
        "8": [],
        # "9": [],
        # "0": [],
    }

    for i, signal in enumerate(signals):
        charset = {c for c in signal}
        if len(signal) == 2:
            counts["1"] = [charset]
        elif len(signal) == 3:
            counts["7"] = [charset]
        elif len(signal) == 4:
            counts["4"] = [charset]

        elif len(signal) == 5:
            counts["5"].append(charset)
        elif len(signal) == 6:
            counts["6"].append(charset)

        elif len(signal) == 7:
            counts["8"] = [charset]

    mapping = {}
    mapping["cf"] = counts["1"][0]
    mapping["a"] = counts["7"][0] - mapping["cf"]

    mapping["bd"] = counts["4"][0] - mapping["cf"]

    mapping["adg"] = counts["5"][0] & counts["5"][1] & counts["5"][2]
    mapping["dg"] = mapping["adg"] - mapping["a"]

    mapping["d"] = mapping["bd"] & mapping["dg"]
    mapping["b"] = mapping["bd"] - mapping["d"]
    mapping["g"] = mapping["dg"] - mapping["d"]

    mapping["bfga"] = counts["6"][0] & counts["6"][1] & counts["6"][2]
    mapping["bfg"] = mapping["bfga"] - mapping["a"]

    mapping["f"] = mapping["cf"] & mapping["bfg"]
    mapping["c"] = mapping["cf"] - mapping["f"]
    mapping["e"] = counts["8"][0] - mapping["a"] - mapping["b"] - mapping["c"] - mapping["d"] - mapping["f"] - mapping["g"]

    mapping = {
        "a": mapping["a"].pop(),
        "b": mapping["b"].pop(),
        "c": mapping["c"].pop(),
        "d": mapping["d"].pop(),
        "e": mapping["e"].pop(),
        "f": mapping["f"].pop(),
        "g": mapping["g"].pop()
    }

    mapped_segments_for_i = {digit: {mapping[seg] for seg in segmets} for digit, segmets in segments_for_i.items()}

    translated_output = []
    for output in outputs:
        if len(output) == 2 or len(output) == 3 or len(output) == 4 or len(output) == 7:
            total1478 += 1

        segments = {c for c in output}
        for digit, segments_needed in mapped_segments_for_i.items():
            if segments == segments_needed:
                translated_output.append(digit)
                break

    value = sum([v * 10 ** i for i, v in enumerate(translated_output[::-1])])
    total += value

print(total1478)
print(total)