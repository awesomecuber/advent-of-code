from math import lcm
from itertools import combinations
import os
import sys

with open(os.path.join(sys.path[0], "day12.txt")) as f:
    puzzle_input = f.read().splitlines()

MOONS = len(puzzle_input)

vertically_split = list(zip(*(line.split('=') for line in puzzle_input)))
moon_x_positions = tuple(int(s[:-3]) for s in vertically_split[1])
moon_y_positions = tuple(int(s[:-3]) for s in vertically_split[2])
moon_z_positions = tuple(int(s[:-1]) for s in vertically_split[3])

moon_x_velocities = (0,) * MOONS
moon_y_velocities = (0,) * MOONS
moon_z_velocities = (0,) * MOONS

def sign(n):
    if n > 0:
        return 1
    if n < 0:
        return -1
    return 0

def update(pos, vel):
    gravities = [0] * MOONS

    for (i, moon_1_pos), (j, moon_2_pos) in combinations(enumerate(pos), 2):
        gravity = sign(moon_2_pos - moon_1_pos) # of moon 1
        gravities[i] += gravity
        gravities[j] -= gravity

    vel = tuple(velocity + gravity for velocity, gravity in zip(vel, gravities))
    pos = tuple(position + velocity for position, velocity in zip(pos, vel))
    return pos, vel

def get_loop_time(pos, vel):
    i = 0
    history = set()
    while (pos, vel) not in history:
        i += 1
        history.add((pos, vel))
        pos, vel = update(pos, vel)
    return i

x = get_loop_time(moon_x_positions, moon_x_velocities)
y = get_loop_time(moon_y_positions, moon_y_velocities)
z = get_loop_time(moon_z_positions, moon_z_velocities)

print(lcm(x, y, z))