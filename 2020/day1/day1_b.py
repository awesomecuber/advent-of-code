from itertools import combinations
import os
import sys

with open(os.path.join(sys.path[0], "day1.txt")) as f:
    puzzle_input = f.read().splitlines()

puzzle_nums = [int(line) for line in puzzle_input]
nums_set = set()

for (num_a, num_b) in combinations(puzzle_nums, 2):
    nums_set.add(num_a + num_b)

working_nums = []

for num in puzzle_nums:
    if (2020 - num) in nums_set:
        working_nums.append(num)

print(working_nums[0] * working_nums[1] * working_nums[2])
