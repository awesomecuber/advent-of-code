import os
import sys

with open(os.path.join(sys.path[0], "day1.txt")) as f:
    puzzle_input = f.read().splitlines()

depths = [int(x) for x in puzzle_input]

depth_windows = [
    depth + next_depth + next_next_depth
    for depth, next_depth, next_next_depth in zip(depths, depths[1:], depths[2:])
]

answer = 0
for depth_window, next_depth_window in zip(depth_windows, depth_windows[1:]):
    if depth_window < next_depth_window:
        answer += 1

print(answer)