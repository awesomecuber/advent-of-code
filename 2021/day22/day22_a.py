from dataclasses import dataclass
from itertools import product
import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day22.txt")) as f:
    puzzle_input = f.read().splitlines()[:20]  # first 20 lines are small


@dataclass
class Instruction:
    turn_on: bool
    x_range: tuple[int, int]
    y_range: tuple[int, int]
    z_range: tuple[int, int]


instructions: list[Instruction] = []

for line in puzzle_input:
    turn_on_str, rest_str = line.split()
    if turn_on_str == "on":
        turn_on = True
    else:
        turn_on = False
    ranges_str = rest_str.split(",")
    x_range = tuple(map(int, ranges_str[0][2:].split("..")))
    y_range = tuple(map(int, ranges_str[1][2:].split("..")))
    z_range = tuple(map(int, ranges_str[2][2:].split("..")))
    instructions.append(Instruction(turn_on, x_range, y_range, z_range))  # type: ignore

on_points: set[tuple[int, int, int]] = set()
for instr in instructions:
    for x, y, z in product(
        range(instr.x_range[0], instr.x_range[1] + 1),
        range(instr.y_range[0], instr.y_range[1] + 1),
        range(instr.z_range[0], instr.z_range[1] + 1),
    ):
        if instr.turn_on:
            on_points.add((x, y, z))
        else:
            on_points.discard((x, y, z))
print(len(on_points))
