import os
import sys

with open(os.path.join(sys.path[0], "day9.txt")) as f:
    puzzle_input = f.read().splitlines()

puzzle_nums = [int(x) for x in puzzle_input]

TARGET = 177777905

start_index = 0
end_index = 1

current = puzzle_nums[start_index]

while current != TARGET:
    if current < TARGET:
        current += puzzle_nums[end_index]
        end_index += 1
    else:
        current -= puzzle_nums[start_index]
        start_index += 1

print(min(puzzle_nums[start_index:end_index]) + max(puzzle_nums[start_index:end_index]))