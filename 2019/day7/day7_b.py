from itertools import permutations, cycle
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

amps = [amp_a, amp_b, amp_c, amp_d, amp_e]

best_output = 0
for phase_settings in permutations(range(5, 10)):
    for amp, phase_setting in zip(amps, phase_settings):
        amp.add_input(phase_setting)

    last_e_output = 0
    output = 0
    for amp in cycle(amps):
        amp.add_input(output)
        output = amp.get_one_output()
        if output is None:
            break
        if amp is amp_e:
            last_e_output = output

    for amp in amps:
        amp.reset()

    best_output = max(best_output, last_e_output)

print(best_output)