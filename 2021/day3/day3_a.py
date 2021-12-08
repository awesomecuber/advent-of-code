import os
import sys

with open(os.path.join(sys.path[0], "day3.txt")) as f:
    puzzle_input = f.read().splitlines()

line_length = len(puzzle_input[0])

num_zeros = [0] * line_length
num_ones = [0] * line_length

for line in puzzle_input:
    for i, bit in enumerate(line):
        match bit:
            case '0':
                num_zeros[i] += 1
            case '1':
                num_ones[i] += 1

print(num_zeros)
print(num_ones)

gamma_rate = ''
epsilon_rate = ''

for num_zero, num_one in zip(num_zeros, num_ones):
    if num_one > num_zero:
        gamma_rate = gamma_rate + '1'
        epsilon_rate = epsilon_rate + '0'
    else:
        gamma_rate = gamma_rate + '0'
        epsilon_rate = epsilon_rate + '1'

print(int(gamma_rate, 2) * int(epsilon_rate, 2))