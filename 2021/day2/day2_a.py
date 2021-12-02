import os
import sys

with open(os.path.join(sys.path[0], "day2.txt")) as f:
    puzzle_input = f.read().splitlines()

horizontal = 0
depth = 0
for line in puzzle_input:
    split_line = line.split()
    command, amount = split_line[0], int(split_line[1])
    match command:
        case "forward":
            horizontal += amount
        case "down":
            depth += amount
        case "up":
            depth -= amount

print(horizontal * depth)
