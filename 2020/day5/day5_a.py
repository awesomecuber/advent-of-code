import os
import sys

with open(os.path.join(sys.path[0], "day5.txt")) as f:
    puzzle_input = f.read().splitlines()

highest_id = 0
for line in puzzle_input:
    row = int(line[:-3].replace("F", "0").replace("B", "1"), 2)
    col = int(line[-3:].replace("L", "0").replace("R", "1"), 2)
    highest_id = max(highest_id, row * 8 + col)
print(highest_id)
