import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day8.txt")) as f:
    puzzle_input = f.read().splitlines()

displays: list[tuple[list[set[str]], list[set[str]]]] = []

for line in puzzle_input:
    unique_signal_patterns, output_value = line.split(' | ')
    displays.append((
        list(map(set, unique_signal_patterns.split())),
        list(map(set, output_value.split()))
    ))

# 0 : 6 lines
# 1 : 2 lines !
# 2 : 5 lines
# 3 : 5 lines
# 4 : 4 lines !
# 5 : 5 lines
# 6 : 6 lines
# 7 : 3 lines !
# 8 : 7 lines !
# 9 : 6 lines

#   0
# 1   2
#   3
# 4   5
#   6

# find digits 1 and 4 and 7 and 8

# step one: establish 0 (7 - 1)
# step two: establish 2/5 (7 & 1)
# step three: establish 1/3 (4 - 1)
# step four: establish 4/6 (8 - (4 & 7))
# step five: establish 0/3/6 (combine all 5-wires)
# step six: establish 3 and 6 with existing info
# step seven: find 5-wire with 4. that is digit 2, use it to find 2

answer = 0
for display in displays:
    wire_segment_connections = [''] * 7

    unique_signal_patterns, output_value = display
    digits = [None] * 10
    five_wires = []
    for pattern in unique_signal_patterns:
        if len(pattern) == 2:
            digits[1] = pattern
        elif len(pattern) == 4:
            digits[4] = pattern
        elif len(pattern) == 3:
            digits[7] = pattern
        elif len(pattern) == 7:
            digits[8] = pattern
        elif len(pattern) == 5:
            five_wires.append(pattern)

    wire_segment_connections[0] = min(digits[7] - digits[1]) # use min to gather only element

    two_five = digits[1] & digits[7]
    one_three = digits[4] - digits[1]
    four_six = digits[8] - (digits[4] | digits[7])
    zero_three_six = five_wires[0] & five_wires[1] & five_wires[2]

    wire_segment_connections[3] = min(one_three & zero_three_six)
    wire_segment_connections[6] = min(four_six & zero_three_six)

    wire_segment_connections[1] = min(one_three - set(wire_segment_connections[3]))
    wire_segment_connections[4] = min(four_six - set(wire_segment_connections[6]))

    for pattern in five_wires:
        if wire_segment_connections[4] in pattern:
            digits[2] = pattern

    wire_segment_connections[2] = min(digits[2] - set(wire_segment_connections))
    wire_segment_connections[5] = min(set('abcdefg') - set(wire_segment_connections))

    digits[0] = set('abcdefg') - set(wire_segment_connections[3])
    digits[3] = set('abcdefg') - set([wire_segment_connections[1], wire_segment_connections[4]])
    digits[5] = set('abcdefg') - set([wire_segment_connections[2], wire_segment_connections[4]])
    digits[6] = set('abcdefg') - set(wire_segment_connections[2])
    digits[9] = set('abcdefg') - set(wire_segment_connections[4])

    output_string = ''
    for val in output_value:
        for n, digit in enumerate(digits):
            if val == digit:
                output_string = output_string + str(n)
    answer += int(output_string)

print(answer)