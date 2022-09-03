import os
import sys

with open(os.path.join(sys.path[0], "day2.txt")) as f:
    puzzle_input = f.read().splitlines()

num_twos = 0
num_threes = 0
for box_id in puzzle_input:
    char_counts: dict[str, int] = {}
    for char in box_id:
        if char not in char_counts:
            char_counts[char] = 0
        char_counts[char] += 1

    pair_seen = False
    triplet_seen = False
    for char, count in char_counts.items():
        if count == 2 and not pair_seen:
            num_twos += 1
            pair_seen = True
        if count == 3 and not triplet_seen:
            num_threes += 1
            triplet_seen = True

print(num_twos * num_threes)
