import os
import sys

with open(os.path.join(sys.path[0], "day9.txt")) as f:
    puzzle_input = f.read().splitlines()

puzzle_nums = [int(x) for x in puzzle_input]

PREAMBLE_SIZE = 25

for i in range(PREAMBLE_SIZE, len(puzzle_nums)):
    nums = puzzle_nums[i - PREAMBLE_SIZE : i]
    target = puzzle_nums[i]
    nums_set = set(nums)

    has_combination = False
    for num in nums:
        if target - num in nums_set:
            has_combination = True
    if not has_combination:
        print(target)
