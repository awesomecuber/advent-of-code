import os
import sys

with open(os.path.join(sys.path[0], "day6.txt")) as f:
    puzzle_input = f.read().splitlines()

fish = [0, 0, 0, 0, 0, 0, 0, 0, 0]
for singular_fish in puzzle_input[0].split(','):
    fish[int(singular_fish)] += 1

for _ in range(256):
    new_fish = fish[0]
    del fish[0]
    fish.append(new_fish)
    fish[6] += new_fish

print(sum(fish))