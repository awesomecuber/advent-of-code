import os
import sys

with open(os.path.join(sys.path[0], "day5.txt")) as f:
    puzzle_input = f.read().splitlines()

slits = [
    [[int(x) for x in coord.split(",")] for coord in line.split(" -> ")]
    for line in puzzle_input
]

points: dict[tuple[int, int], int] = {}


def add_point(point):
    if point not in points:
        points[point] = 0
    points[point] += 1


for slit in slits:
    (x1, y1), (x2, y2) = slit
    if x1 == x2:
        if y1 < y2:
            for y in range(y1, y2 + 1):
                add_point((x1, y))
        else:
            for y in range(y1, y2 - 1, -1):
                add_point((x1, y))
    elif y1 == y2:
        if x1 < x2:
            for x in range(x1, x2 + 1):
                add_point((x, y1))
        else:
            for x in range(x1, x2 - 1, -1):
                add_point((x, y1))

total_overlaps = 0
for slits in points.values():
    if slits > 1:
        total_overlaps += 1
print(total_overlaps)
