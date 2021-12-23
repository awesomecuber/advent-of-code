from dataclasses import dataclass
from itertools import product
import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day22.txt")) as f:
    puzzle_input = f.read().splitlines()

@dataclass
class Cube:
    x_range: tuple[int, int]
    y_range: tuple[int, int]
    z_range: tuple[int, int]

@dataclass
class Instruction:
    turn_on: bool
    cube: Cube

def split_cube(to_split: Cube, other: Cube) -> set[Cube]:
    to_return: set[Cube] = set()
    if to_split.x_range[0]:
        pass
    return to_return

instructions: list[Instruction] = []

for line in puzzle_input:
    turn_on_str, rest_str = line.split()
    if turn_on_str == 'on':
        turn_on = True
    else:
        turn_on = False
    ranges_str = rest_str.split(',')
    x_range = tuple(map(int, ranges_str[0][2:].split('..')))
    y_range = tuple(map(int, ranges_str[1][2:].split('..')))
    z_range = tuple(map(int, ranges_str[2][2:].split('..')))
    instructions.append(Instruction(turn_on, Cube(x_range, y_range, z_range))) # type: ignore

print(instructions)

on_cubes: set[Cube] = set()
for instr in instructions:
    pass
print(len(on_cubes))