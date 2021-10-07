import copy
import itertools
import os
import sys

with open(os.path.join(sys.path[0], "day17.txt")) as f:
    puzzle_input = f.read().splitlines()

active_cubes = set()

for y, line in enumerate(puzzle_input):
    for x, character in enumerate(line):
        if character == "#":
            active_cubes.add((x, y, 0))

for i in range(6):
    all_x = [x[0] for x in active_cubes]
    range_x = range(min(all_x) - 1, max(all_x) + 2)

    all_y = [x[1] for x in active_cubes]
    range_y = range(min(all_y) - 1, max(all_y) + 2)

    all_z = [x[2] for x in active_cubes]
    range_z = range(min(all_z) - 1, max(all_z) + 2)

    active_old_cubes = copy.deepcopy(active_cubes)
    for cube in itertools.product(range_x, range_y, range_z):
        surrounding_cubes = 0
        for x_del, y_del, z_del in itertools.product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1]):
            if not x_del == y_del == z_del == 0:
                if (cube[0] + x_del, cube[1] + y_del, cube[2] + z_del) in active_old_cubes:
                    surrounding_cubes += 1
        if cube in active_old_cubes:
            if not surrounding_cubes in [2, 3]:
                active_cubes.remove(cube)
        else:
            if surrounding_cubes == 3:
                active_cubes.add(cube)
print(len(active_cubes))