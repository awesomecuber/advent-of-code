import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day8.txt")) as f:
    puzzle_input = f.read().splitlines()

displays: list[tuple[list[str], list[str]]] = []

for line in puzzle_input:
    unique_signal_patterns, output_value = line.split(' | ')
    displays.append((unique_signal_patterns.split(), output_value.split()))

answer = 0
for display in displays:
    output_value = display[1]
    for val in output_value:
        if len(val) in [2, 4, 3, 7]:
            answer += 1

print(answer)