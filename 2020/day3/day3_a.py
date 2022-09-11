import os
import sys

with open(os.path.join(sys.path[0], "day3.txt")) as f:
    puzzle_input = f.read().splitlines()

horizontal_position = 0
num_trees = 0
for line in puzzle_input:
    if line[horizontal_position % len(line)] == "#":
        num_trees += 1
    horizontal_position += 3
print(num_trees)
