import os
import sys

with open(os.path.join(sys.path[0], "day8.txt")) as f:
    puzzle_input = f.read().splitlines()

lines_visited = set()
accumulator = 0
line = 0

while line not in lines_visited:
    lines_visited.add(line)
    instruction = puzzle_input[line][:3]
    value = int(puzzle_input[line][4:])
    if instruction == "acc":
        accumulator += value
        line += 1
    elif instruction == "jmp":
        line += value
    elif instruction == "nop":
        line += 1
    else:
        print("problem")

print(accumulator)