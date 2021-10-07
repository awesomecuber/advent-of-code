import os
import sys

with open(os.path.join(sys.path[0], "day1.txt")) as f:
    puzzle_input = f.read().splitlines()

masses = [int(x) for x in puzzle_input]

total_fuel = 0

for mass in masses:
    fuel = (mass // 3) - 2
    total_fuel += fuel

print(total_fuel)