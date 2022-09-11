import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day11.txt")) as f:
    puzzle_input = f.read().splitlines()

energy_levels: list[list[int]] = [[int(y) for y in list(x)] for x in puzzle_input]

adjacents = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

max_x = len(energy_levels[0])
max_y = len(energy_levels)

cur_step = 0
while True:
    for y, line in enumerate(energy_levels):
        for x, energy in enumerate(line):
            energy_levels[y][x] += 1
    done_flashing = False
    flashes_this_step = 0
    while not done_flashing:
        done_flashing = True
        for y, line in enumerate(energy_levels):
            for x, energy in enumerate(line):
                if energy_levels[y][x] >= 10:
                    flashes_this_step += 1
                    energy_levels[y][x] = 0
                    done_flashing = False
                    for adjacent in adjacents:
                        other_x = x + adjacent[0]
                        other_y = y + adjacent[1]
                        if (
                            0 <= other_x < max_x
                            and 0 <= other_y < max_y
                            and energy_levels[other_y][other_x] != 0
                        ):
                            energy_levels[other_y][other_x] += 1
    cur_step += 1
    if flashes_this_step == max_x * max_y:
        print(cur_step)
        break
