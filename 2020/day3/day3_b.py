import os
import sys

with open(os.path.join(sys.path[0], "day3.txt")) as f:
    puzzle_input = f.read().splitlines()

def get_tree(right, down):
    horizontal_position = 0
    num_trees = 0
    for line in puzzle_input[::down]:
        if line[horizontal_position % len(line)] == "#":
            num_trees += 1
        horizontal_position += right
    return num_trees

print(get_tree(1, 1) * get_tree(3, 1) * get_tree(5, 1) * get_tree(7, 1) * get_tree(1, 2))