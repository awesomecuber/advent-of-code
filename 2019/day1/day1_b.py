import os
import sys

with open(os.path.join(sys.path[0], "day1.txt")) as f:
    puzzle_input = f.read().splitlines()

masses = [int(x) for x in puzzle_input]


def find_fuel(mass):
    total_fuel = 0
    next_fuel = (mass // 3) - 2
    while next_fuel >= 0:
        total_fuel += next_fuel
        next_fuel = (next_fuel // 3) - 2
    return total_fuel


total_fuel = 0
for mass in masses:
    total_fuel += find_fuel(mass)

print(total_fuel)
