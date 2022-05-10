import os
import sys

with open(os.path.join(sys.path[0], "day8.txt")) as f:
    puzzle_input = f.read()

layers = []

while len(puzzle_input) > 0:
    layers.append([int(char) for char in puzzle_input[:25 * 6]])
    puzzle_input = puzzle_input[25 * 6:]

def num_of_digit(arr, digit):
    return len([x for x in arr if x == digit])

fewest_zero_count = min(num_of_digit(layer, 0) for layer in layers)
fewest_zero_layer = [layer for layer in layers if num_of_digit(layer, 0) == fewest_zero_count][0]

print(num_of_digit(fewest_zero_layer, 1) * num_of_digit(fewest_zero_layer, 2))