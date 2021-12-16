import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day9.txt")) as f:
    puzzle_input = f.read().splitlines()

heightmap: list[str] = puzzle_input

adjacents = [(-1, 0), (1, 0), (0, -1), (0, 1)]

max_x = len(heightmap[0])
max_y = len(heightmap)

total_risk_level = 0
for y, line in enumerate(heightmap):
    for x, location in enumerate(line):
        height = int(location)
        adjacent_heights = []
        for adjacent in adjacents:
            other_x = x + adjacent[0]
            other_y = y + adjacent[1]
            if 0 <= other_x < max_x and 0 <= other_y < max_y:
                adjacent_heights.append(int(heightmap[other_y][other_x]))
        if height < min(adjacent_heights):
            total_risk_level += height + 1
print(total_risk_level)