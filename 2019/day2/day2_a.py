import os
import sys

with open(os.path.join(sys.path[0], "day2.txt")) as f:
    puzzle_input = f.read()

numbers = [int(x) for x in puzzle_input.split(",")]
numbers[1] = 12
numbers[2] = 2

current_index = 0
while numbers[current_index] != 99:
    if numbers[current_index] == 1:
        first_input = numbers[numbers[current_index + 1]]
        second_input = numbers[numbers[current_index + 2]]
        output_index = numbers[current_index + 3]
        numbers[output_index] = first_input + second_input
    elif numbers[current_index] == 2:
        first_input = numbers[numbers[current_index + 1]]
        second_input = numbers[numbers[current_index + 2]]
        output_index = numbers[current_index + 3]
        numbers[output_index] = first_input * second_input
    current_index += 4

print(numbers[0])