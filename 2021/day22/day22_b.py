from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from operator import mul
import os
import sys

with open(os.path.join(sys.path[0], "day22.txt")) as f:
    puzzle_input = f.read().splitlines()

@dataclass(frozen=True)
class Range:
    min: int
    max: int

# actually rectangular prism
@dataclass(frozen=True)
class Cube:
    ranges: tuple[Range, Range, Range]

    def size(self) -> int:
        return reduce(mul, (range.max - range.min + 1 for range in self.ranges))

    def __repr__(self) -> str:
        return (
            f'x={self.ranges[0].min}..{self.ranges[0].max},'
            f'y={self.ranges[1].min}..{self.ranges[1].max},'
            f'z={self.ranges[2].min}..{self.ranges[2].max}'
        )

@dataclass
class Instruction:
    turn_on: bool
    cube: Cube

def split_cube(to_split: Cube, other: Cube) -> set[Cube]:
    to_return: set[Cube] = set()
    to_return.add(to_split)
    # first, cut along x dimension
    # for every split cube (redundant for first dimension but whatevs):
    #
    for n, other_range in enumerate(other.ranges):
        new_to_return: set[Cube] = set()
        for split_cube in to_return:
            split_range = split_cube.ranges[n]
            split_points: list[int] = []
            if split_range.min < other_range.min <= split_range.max:
                split_points.append(other_range.min)
            if split_range.min <= other_range.max < split_range.max:
                split_points.append(other_range.max + 1)

            if len(split_points) == 0:
                new_to_return.add(deepcopy(split_cube))
            if len(split_points) == 1:
                new_ranges = list(split_cube.ranges)
                new_ranges[n] = Range(split_range.min, split_points[0] - 1)
                new_to_return.add(Cube(tuple(new_ranges))) # type: ignore
                new_ranges[n] = Range(split_points[0], split_range.max)
                new_to_return.add(Cube(tuple(new_ranges))) # type: ignore
            elif len(split_points) == 2:
                new_ranges = list(split_cube.ranges)
                new_ranges[n] = Range(split_range.min, split_points[0] - 1)
                new_to_return.add(Cube(tuple(new_ranges))) # type: ignore
                new_ranges[n] = Range(split_points[0], split_points[1] - 1)
                new_to_return.add(Cube(tuple(new_ranges))) # type: ignore
                new_ranges[n] = Range(split_points[1], split_range.max)
                new_to_return.add(Cube(tuple(new_ranges))) # type: ignore
        to_return = new_to_return
    return to_return

def cubes_intersect(cube1: Cube, cube2: Cube):
    return all(
        range1.max >= range2.min and range1.min <= range2.max
        for range1, range2 in zip(cube1.ranges, cube2.ranges)
    )

instructions: list[Instruction] = []

for line in puzzle_input:
    turn_on_str, rest_str = line.split()
    if turn_on_str == 'on':
        turn_on = True
    else:
        turn_on = False
    ranges_str = rest_str.split(',')
    x_range = Range(*map(int, ranges_str[0][2:].split('..')))
    y_range = Range(*map(int, ranges_str[1][2:].split('..')))
    z_range = Range(*map(int, ranges_str[2][2:].split('..')))
    instructions.append(Instruction(turn_on, Cube((x_range, y_range, z_range)))) # type: ignore

on_cubes: set[Cube] = set()
for i, instr in enumerate(instructions):
    # print(i, len(on_cubes))
    intersecting_cubes = set(cube for cube in on_cubes if cubes_intersect(cube, instr.cube))
    for intersecting_cube in intersecting_cubes:
        on_cubes.remove(intersecting_cube)
        readd_cubes = split_cube(intersecting_cube, instr.cube)
        readd_cubes = set(
            cube for cube in readd_cubes
            if not cubes_intersect(cube, instr.cube)
        )
        on_cubes |= readd_cubes
    if instr.turn_on:
        on_cubes.add(instr.cube)

print(sum(cube.size() for cube in on_cubes))
