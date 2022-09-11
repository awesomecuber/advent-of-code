import os
import sys

with open(os.path.join(sys.path[0], "day7.txt")) as f:
    puzzle_input = f.read().splitlines()

crab_positions = list(map(int, puzzle_input[0].split(",")))

min_position = min(crab_positions)
max_position = max(crab_positions)

best_congregation_position = -1
best_fuel_cost = sys.maxsize
for congregation_position in range(min_position, max_position + 1):
    fuel_cost = 0
    for crab_position in crab_positions:
        distance = abs(crab_position - congregation_position)
        fuel_cost += distance * (distance + 1) // 2
    if fuel_cost < best_fuel_cost:
        best_congregation_position = congregation_position
        best_fuel_cost = fuel_cost

print(best_fuel_cost)
