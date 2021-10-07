import itertools
import os
import sys

with open(os.path.join(sys.path[0], "day5.txt")) as f:
    puzzle_input = f.read()

original_numbers = [int(x) for x in puzzle_input.split(",")]

for noun, verb in itertools.product(range(100), range(100)):
    current_index = 0
    numbers = original_numbers.copy()
    numbers[1] = noun
    numbers[2] = verb
    while numbers[current_index] != 99:
        first_input = numbers[numbers[current_index + 1]]
        second_input = numbers[numbers[current_index + 2]]
        output_index = numbers[current_index + 3]
        if numbers[current_index] == 1:
            numbers[output_index] = first_input + second_input
        elif numbers[current_index] == 2:
            numbers[output_index] = first_input * second_input
        current_index += 4
    if numbers[0] == 19690720:
        print(100 * noun + verb)
        break