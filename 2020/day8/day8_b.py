import os
import sys

with open(os.path.join(sys.path[0], "day8.txt")) as f:
    puzzle_input = f.read().splitlines()

lines_visited = set()
accumulator = 0
line = 0

for possible_error_line, possible_error in enumerate(puzzle_input):
    error_instruction = possible_error[:3]
    if error_instruction in ["jmp", "nop"]:
        fixed_instruction = ""
        if error_instruction == "jmp":
            fixed_instruction = "nop"
        else:
            fixed_instruction = "jmp"
        new_instructions = puzzle_input.copy()
        new_instructions[possible_error_line] = fixed_instruction + possible_error[3:]

        lines_visited = set()
        accumulator = 0
        line = 0
        while line not in lines_visited and line != len(new_instructions):
            lines_visited.add(line)
            instruction = new_instructions[line][:3]
            value = int(new_instructions[line][4:])
            if instruction == "acc":
                accumulator += value
                line += 1
            elif instruction == "jmp":
                line += value
            elif instruction == "nop":
                line += 1
            else:
                print("problem")
        if line == len(new_instructions):
            print(accumulator)
