import os
import sys

with open(os.path.join(sys.path[0], "day5.txt")) as f:
    puzzle_input = f.read().splitlines()

ids = set()
for line in puzzle_input:
    row = int(line[:-3].replace("F", "0").replace("B", "1"), 2)
    col = int(line[-3:].replace("L", "0").replace("R", "1"), 2)
    ids.add(row * 8 + col)

for i in range(1, 861):
    if i not in ids and (i - 1 in ids and i + 1 in ids):
        print(i)
