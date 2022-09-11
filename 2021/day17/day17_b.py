from itertools import product
import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day17.txt")) as f:
    puzzle_input = f.readline()

puzzle_input = puzzle_input[puzzle_input.index("x=") :]
x_range, y_range = puzzle_input.split(", ")
x_vals = x_range[2:].split("..")
y_vals = y_range[2:].split("..")

min_x = int(x_vals[0])
max_x = int(x_vals[1])
min_y = int(y_vals[0])
max_y = int(y_vals[1])

low_x_vel = 1
high_x_vel = max_x + 1
low_y_vel = min_y - 1
high_y_vel = -min_y - 1

hits = 0
for x_vel, y_vel in product(
    range(low_x_vel, high_x_vel + 1), range(low_y_vel, high_y_vel + 1)
):
    x = 0
    y = 0
    while True:
        x += x_vel
        y += y_vel
        if x_vel > 0:
            x_vel -= 1
        if x_vel < 0:
            x_vel += 1
        y_vel -= 1
        if min_x <= x <= max_x and min_y <= y <= max_y:
            hits += 1
            break
        if x > max_x or y < min_y:
            break

print(hits)
