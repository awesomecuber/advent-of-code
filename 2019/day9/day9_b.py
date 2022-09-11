import os
import sys

from intcode import IntCodeProgram

with open(os.path.join(sys.path[0], "day9.txt")) as f:
    puzzle_input = f.read()

memory = [int(x) for x in puzzle_input.split(",")]

program = IntCodeProgram(memory)

print(program.run([2]))
