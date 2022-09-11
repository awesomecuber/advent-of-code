import os
import sys

with open(os.path.join(sys.path[0], "day13.txt")) as f:
    puzzle_input = f.read().splitlines()

starting_timestamp = int(puzzle_input[0])
bus_ids = [int(x) for x in puzzle_input[1].split(",") if x != "x"]

timestamp = starting_timestamp
found = False
while not found:
    for bus_id in bus_ids:
        if timestamp % bus_id == 0:
            print((timestamp - starting_timestamp) * bus_id)
            found = True
    timestamp += 1
