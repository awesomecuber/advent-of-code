from itertools import combinations
import os
import sys

with open(os.path.join(sys.path[0], "day2sarah.txt")) as f:
    puzzle_input = f.read().splitlines()

for first, second in combinations(puzzle_input, 2):
    diff_seen = False
    diff_at = 0
    for i, (char1, char2) in enumerate(zip(first, second)):
        if char1 != char2:
            if diff_seen:
                break
            diff_seen = True
            diff_at = i
    else:
        print(first[:diff_at] + first[diff_at+1:])
