import os
import sys

with open(os.path.join(sys.path[0], "day3.txt")) as f:
    puzzle_input = f.read().splitlines()

line_length = len(puzzle_input[0])

possible_oxygen_generator_ratings = puzzle_input.copy()
possible_co2_scrubber_ratings = puzzle_input.copy()

cur_bit = 0
while len(possible_oxygen_generator_ratings) > 1:
    num_zeros = 0
    num_ones = 0
    for line in possible_oxygen_generator_ratings:
        match line[cur_bit]:
            case '0':
                num_zeros += 1
            case '1':
                num_ones += 1
    new_arr = []
    for line in possible_oxygen_generator_ratings:
        if line[cur_bit] == '0' and num_zeros > num_ones:
            new_arr.append(line)
        if line[cur_bit] == '1' and num_zeros <= num_ones:
            new_arr.append(line)
    possible_oxygen_generator_ratings = new_arr
    cur_bit += 1

cur_bit = 0
while len(possible_co2_scrubber_ratings) > 1:
    num_zeros = 0
    num_ones = 0
    for line in possible_co2_scrubber_ratings:
        match line[cur_bit]:
            case '0':
                num_zeros += 1
            case '1':
                num_ones += 1
    new_arr = []
    for line in possible_co2_scrubber_ratings:
        if line[cur_bit] == '0' and num_zeros <= num_ones:
            new_arr.append(line)
        if line[cur_bit] == '1' and num_zeros > num_ones:
            new_arr.append(line)
    possible_co2_scrubber_ratings = new_arr
    cur_bit += 1

oxygen_generator_rating = possible_oxygen_generator_ratings[0]
co2_scrubber_rating = possible_co2_scrubber_ratings[0]

print(int(oxygen_generator_rating, 2) * int(co2_scrubber_rating, 2))