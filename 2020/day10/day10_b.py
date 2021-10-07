import os
import sys
import time

with open(os.path.join(sys.path[0], "day10.txt")) as f:
    puzzle_input = f.read().splitlines()

nums_set = set([int(x) for x in puzzle_input])
goal = max(nums_set) + 3

nums_set.add(0)
nums_set.add(goal)

start_time = time.time()

calculated = {}
def count_arrangements(start):
    if start == goal:
        return 1
    if start in calculated:
        return calculated[start]
    to_return = 0
    if start + 1 in nums_set:
        to_return += count_arrangements(start + 1)
    if start + 2 in nums_set:
        to_return += count_arrangements(start + 2)
    if start + 3 in nums_set:
        to_return += count_arrangements(start + 3)
    calculated[start] = to_return
    return to_return

arrangements = count_arrangements(0)
print(time.time() - start_time)
print(arrangements)