import functools
import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day9.txt")) as f:
    puzzle_input = f.read().splitlines()

heightmap: list[str] = puzzle_input

adjacents = [(-1, 0), (1, 0), (0, -1), (0, 1)]

max_x = len(heightmap[0])
max_y = len(heightmap)

flows_to: dict[tuple[int, int], tuple[int, int]] = {}
for y, line in enumerate(heightmap):
    for x, height in enumerate(line):
        if int(height) == 9:
            continue
        cur_location = (x, y)
        cur_height = int(height)
        low_point_found = False
        while not low_point_found:
            next_location = None
            next_height = None
            for adjacent in adjacents:
                other_x = cur_location[0] + adjacent[0]
                other_y = cur_location[1] + adjacent[1]
                if 0 <= other_x < max_x and 0 <= other_y < max_y:
                    other_height = int(heightmap[other_y][other_x])
                    if other_height < cur_height:
                        next_location = (other_x, other_y)
                        next_height = other_height
                        break
            if next_location is None:
                low_point_found = True
                flows_to[(x, y)] = cur_location
            cur_location = next_location
            cur_height = next_height

basin_sizes: dict[tuple[int, int], int] = {}
for low_point in flows_to.values():
    if low_point not in basin_sizes:
        basin_sizes[low_point] = 0
    basin_sizes[low_point] += 1

print(
    functools.reduce(lambda x, y: x * y, sorted(basin_sizes.values(), reverse=True)[:3])
)
