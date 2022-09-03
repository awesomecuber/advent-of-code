from collections import defaultdict
import os
import sys

with open(os.path.join(sys.path[0], "day3.txt")) as f:
    puzzle_input = f.read().splitlines()

coords_times: dict[tuple[int, int], int] = defaultdict(int)
for line in puzzle_input:
    line_parts = line.split()
    coords = line_parts[2][:-1].split(",")
    x, y = int(coords[0]), int(coords[1])
    size = line_parts[3].split("x")
    w, h = int(size[0]), int(size[1])

    for i in range(h):
        for j in range(w):
            coords_times[(x+j, y+i)] += 1

answer = 0
for count in coords_times.values():
    if count >= 2:
        answer += 1

print(answer)
