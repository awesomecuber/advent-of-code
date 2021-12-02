import os
import sys

with open(os.path.join(sys.path[0], "day2ex.txt")) as f:
    puzzle_input = f.read().splitlines()

horizontal = 0
depth = 0
aim = 0
for line in puzzle_input:
    split_line = line.split()
    command, amount = split_line[0], int(split_line[1])
    match command:
        case "forward":
            horizontal += amount
            depth += aim * amount
        case "down":
            aim += amount
        case "up":
            aim -= amount

print(horizontal * depth)
