import os
import sys

with open(os.path.join(sys.path[0], "day12.txt")) as f:
    puzzle_input = f.read().splitlines()

ship_position = [0, 0]
waypoint_position = [10, 1]
for line in puzzle_input:
    command = line[:1]
    amount = int(line[1:])
    if command == "N":
        waypoint_position[1] += amount
    elif command == "S":
        waypoint_position[1] -= amount
    elif command == "E":
        waypoint_position[0] += amount
    elif command == "W":
        waypoint_position[0] -= amount
    elif command in ["L", "R"]:
        if line in ["R90", "L270"]:
            waypoint_position = [waypoint_position[1], -waypoint_position[0]]
        if line in ["R180", "L180"]:
            waypoint_position = [-waypoint_position[0], -waypoint_position[1]]
        if line in ["R270", "L90"]:
            waypoint_position = [-waypoint_position[1], waypoint_position[0]]
    elif command == "F":
        ship_position[0] += amount * waypoint_position[0]
        ship_position[1] += amount * waypoint_position[1]

print(abs(ship_position[0]) + abs(ship_position[1]))