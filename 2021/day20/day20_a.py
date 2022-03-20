from itertools import product
import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day20.txt")) as f:
    puzzle_input = f.read().splitlines()

to_turn_on = set()
for i, char in enumerate(puzzle_input[0]):
    if char == '#':
        to_turn_on.add(i)

on_pixels = set()
for y, line in enumerate(puzzle_input[2:]):
    for x, char in enumerate(line):
        if char == '#':
            on_pixels.add((x, y))

def print_image(on_pixels):
    min_x = min(x for x, _ in on_pixels)
    max_x = max(x for x, _ in on_pixels)
    min_y = min(y for _, y in on_pixels)
    max_y = max(y for _, y in on_pixels)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in on_pixels:
                print('#', end='')
            else:
                print('.', end='')
        print()

background_on = False
# print_image(on_pixels)

for i in range(2):
    MARGIN = 1
    min_x = min(x for x, _ in on_pixels)
    max_x = max(x for x, _ in on_pixels)
    min_y = min(y for _, y in on_pixels)
    max_y = max(y for _, y in on_pixels)

    next_on_pixels = set()
    for x, y in product(range(min_x - MARGIN, max_x + MARGIN + 1), range(min_y - MARGIN, max_y + MARGIN + 1)):
        bin_num = ''
        for dy, dx in product(range(-1, 2), repeat=2):
            if x + dx < min_x or x + dx > max_x or y + dy < min_y or y + dy > max_y:
                if not background_on:
                    bin_num = bin_num + '0'
                else:
                    bin_num = bin_num + '1'
            elif (x + dx, y + dy) in on_pixels:
                bin_num = bin_num + '1'
            else:
                bin_num = bin_num + '0'
        if int(bin_num, 2) in to_turn_on:
            next_on_pixels.add((x, y))

    if not background_on and 0 in to_turn_on:
        background_on = True
    elif background_on and 511 not in to_turn_on:
        background_on = False
    on_pixels = next_on_pixels

print(len(on_pixels))
# print_image(on_pixels)
# print()