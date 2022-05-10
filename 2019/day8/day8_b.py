import os
import sys

with open(os.path.join(sys.path[0], "day8.txt")) as f:
    puzzle_input = f.read()

layers = []

while len(puzzle_input) > 0:
    layers.append([int(char) for char in puzzle_input[:25 * 6]])
    puzzle_input = puzzle_input[25 * 6:]

image = []
for pixel_stack in zip(*layers):
    for pixel in pixel_stack:
        if pixel in [0, 1]:
            image.append(pixel)
            break

while len(image) > 0:
    for pixel in image[:25]:
        if pixel == 0:
            print('.', end='')
        if pixel == 1:
            print('#', end='')
    print()
    image = image[25:]