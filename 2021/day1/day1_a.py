import os
import sys

with open(os.path.join(sys.path[0], "day1.txt")) as f:
    puzzle_input = f.read().splitlines()

depths = [int(x) for x in puzzle_input]

answer = 0
for depth, next_depth in zip(depths, depths[1:]):
    if depth < next_depth:
        answer += 1

print(answer)
