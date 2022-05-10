from itertools import permutations
import os
import sys

from intcode import IntCodeProgram

with open(os.path.join(sys.path[0], "day7.txt")) as f:
    puzzle_input = f.read()

numbers = [int(x) for x in puzzle_input.split(",")]

amp_a = IntCodeProgram(numbers)
amp_b = IntCodeProgram(numbers)
amp_c = IntCodeProgram(numbers)
amp_d = IntCodeProgram(numbers)
amp_e = IntCodeProgram(numbers)

best_output = 0
for phase_settings in permutations(range(5)):
    output = 0
    for i, amp in enumerate([amp_a, amp_b, amp_c, amp_d, amp_e]):
        output = amp.run([phase_settings[i], output])[0]
    best_output = max(best_output, output)

print(best_output)