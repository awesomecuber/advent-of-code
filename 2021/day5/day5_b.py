import os
import sys

with open(os.path.join(sys.path[0], "day5.txt")) as f:
    puzzle_input = f.read().splitlines()

slits = [[[int(x) for x in coord.split(',')] for coord in line.split(' -> ')] for line in puzzle_input]

points: dict[tuple[int, int], int] = {}

def add_point(point):
    if point not in points:
        points[point] = 0
    points[point] += 1

for slit in slits:
    (x1, y1), (x2, y2) = slit
    low_x = min(x1, x2)
    high_x = max(x1, x2)
    low_y = min(y1, y2)
    high_y = max(y1, y2)

    if low_x == high_x:
        for y in range(low_y, high_y + 1):
            add_point((low_x, y))
    elif low_y == high_y:
        for x in range(low_x, high_x + 1):
            add_point((x, low_y))
    else:
        if x1 - x2 == y1 - y2:
            for offset in range(0, high_x - low_x + 1):
                add_point((low_x + offset, low_y + offset))
        else:
            for offset in range(0, high_x - low_x + 1):
                add_point((high_x - offset, low_y + offset))

total_overlaps = 0
for slits in points.values():
    if slits > 1:
        total_overlaps += 1
print(total_overlaps)