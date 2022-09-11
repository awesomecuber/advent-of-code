import os
import sys

with open(os.path.join(sys.path[0], "day3.txt")) as f:
    puzzle_input = f.read().splitlines()

wire_one_instructions = puzzle_input[0].split(",")
wire_two_instructions = puzzle_input[1].split(",")


def get_wire_locations(wire_instructions):
    wire_locations = set()
    current_coord = [0, 0]
    for instruction in wire_instructions:
        if instruction[0] == "U":
            for i in range(int(instruction[1:])):
                current_coord[1] += 1
                wire_locations.add(tuple(current_coord))
        elif instruction[0] == "D":
            for i in range(int(instruction[1:])):
                current_coord[1] -= 1
                wire_locations.add(tuple(current_coord))
        elif instruction[0] == "L":
            for i in range(int(instruction[1:])):
                current_coord[0] -= 1
                wire_locations.add(tuple(current_coord))
        elif instruction[0] == "R":
            for i in range(int(instruction[1:])):
                current_coord[0] += 1
                wire_locations.add(tuple(current_coord))
    return wire_locations


intersections = get_wire_locations(wire_one_instructions) & get_wire_locations(
    wire_two_instructions
)

print(min(abs(x) + abs(y) for x, y in intersections))
