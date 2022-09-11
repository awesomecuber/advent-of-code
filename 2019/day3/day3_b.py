import os
import sys

with open(os.path.join(sys.path[0], "day3.txt")) as f:
    puzzle_input = f.read().splitlines()

wire_one_instructions = puzzle_input[0].split(",")
wire_two_instructions = puzzle_input[1].split(",")


def get_wire_locations(wire_instructions):
    wire_locations = {}
    current_coord = [0, 0]
    current_step = 0
    for instruction in wire_instructions:
        if instruction[0] == "U":
            for i in range(int(instruction[1:])):
                current_coord[1] += 1
                current_step += 1
                wire_locations[tuple(current_coord)] = current_step
        elif instruction[0] == "D":
            for i in range(int(instruction[1:])):
                current_coord[1] -= 1
                current_step += 1
                wire_locations[tuple(current_coord)] = current_step
        elif instruction[0] == "L":
            for i in range(int(instruction[1:])):
                current_coord[0] -= 1
                current_step += 1
                wire_locations[tuple(current_coord)] = current_step
        elif instruction[0] == "R":
            for i in range(int(instruction[1:])):
                current_coord[0] += 1
                current_step += 1
                wire_locations[tuple(current_coord)] = current_step
    return wire_locations


one = get_wire_locations(wire_one_instructions)
two = get_wire_locations(wire_two_instructions)
intersections = one.keys() & two.keys()

print(min(one[(x, y)] + two[(x, y)] for x, y in intersections))
