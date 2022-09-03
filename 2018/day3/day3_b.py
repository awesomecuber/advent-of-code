from collections import defaultdict
import os
import sys

with open(os.path.join(sys.path[0], "day3.txt")) as f:
    puzzle_input = f.read().splitlines()


def get_data(line: str) -> tuple[int, int, int, int, int]:
    line_parts = line.split()
    id = int(line_parts[0][1:])
    coords = line_parts[2][:-1].split(",")
    x, y = int(coords[0]), int(coords[1])
    size = line_parts[3].split("x")
    w, h = int(size[0]), int(size[1])
    return id, x, y, w, h


coords_times: dict[tuple[int, int], int] = defaultdict(int)
for line in puzzle_input:
    _, x, y, w, h = get_data(line)
    for i in range(h):
        for j in range(w):
            coords_times[(x+j, y+i)] += 1

for line in puzzle_input:
    id, x, y, w, h = get_data(line)
    no_overlap = True
    for i in range(h):
        for j in range(w):
            if coords_times[(x+j, y+i)] != 1:
                no_overlap = False
    if no_overlap:
        print(id)
        break
