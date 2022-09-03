from itertools import cycle
import os
import sys

with open(os.path.join(sys.path[0], "day1.txt")) as f:
    puzzle_input = f.read().splitlines()

nums = list(map(int, puzzle_input))

freq = 0
already_seen = set()
for num in cycle(nums):
    already_seen.add(freq)
    freq += num
    if freq in already_seen:
        break

print(freq)
