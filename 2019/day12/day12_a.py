from itertools import combinations
import os
import sys

with open(os.path.join(sys.path[0], "day12.txt")) as f:
    puzzle_input = f.read().splitlines()

moon_positions = []
for line in puzzle_input:
    split_line = line.split("=")
    moon_x = int(split_line[1][:-3])
    moon_y = int(split_line[2][:-3])
    moon_z = int(split_line[3][:-1])
    moon_positions.append((moon_x, moon_y, moon_z))

moon_velocities = [(0, 0, 0)] * len(moon_positions)


def sign(n):
    if n > 0:
        return 1
    if n < 0:
        return -1
    return 0


def add_tuples(tuple_1, tuple_2):
    return tuple(a + b for a, b in zip(tuple_1, tuple_2))


def subtract_tuples(tuple_1, tuple_2):
    return tuple(a - b for a, b in zip(tuple_1, tuple_2))


for _ in range(1000):
    gravities = [(0, 0, 0)] * len(moon_positions)

    for (i, moon_1_pos), (j, moon_2_pos) in combinations(enumerate(moon_positions), 2):
        pos_dif = subtract_tuples(moon_2_pos, moon_1_pos)
        gravity = tuple(map(sign, pos_dif))  # of moon 1
        gravities[i] = add_tuples(gravities[i], gravity)
        gravities[j] = subtract_tuples(gravities[j], gravity)

    moon_velocities = [
        add_tuples(velocity, gravity)
        for velocity, gravity in zip(moon_velocities, gravities)
    ]
    moon_positions = [
        add_tuples(position, velocity)
        for position, velocity in zip(moon_positions, moon_velocities)
    ]


def energy(pos, vel):
    potential_energy = abs(pos[0]) + abs(pos[1]) + abs(pos[2])
    kinetic_energy = abs(vel[0]) + abs(vel[1]) + abs(vel[2])
    return potential_energy * kinetic_energy


print(sum(energy(pos, vel) for pos, vel in zip(moon_positions, moon_velocities)))
