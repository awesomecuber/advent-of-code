import os
import sys

with open(os.path.join(sys.path[0], "day16.txt")) as f:
    puzzle_input = f.read().splitlines()

classes = {} # maps class name to ((a, b), (a, b))
nearby_tickets = []

first_space = puzzle_input.index("")
classes_input = puzzle_input[:first_space]

for class_input in classes_input:
    first_split = class_input.split(": ")
    name = first_split[0]
    second_split = first_split[1].split(" or ")
    interval_one = tuple([int(x) for x in second_split[0].split("-")])
    interval_two = tuple([int(x) for x in second_split[1].split("-")])
    classes[name] = (interval_one, interval_two)

my_ticket = [int(x) for x in puzzle_input[first_space + 2].split(",")]
nearby_tickets = [[int(y) for y in x.split(",")] for x in puzzle_input[first_space + 5:]]

all_intervals = [y for x in classes for y in classes[x]]
print(all_intervals)

error_rate = 0
for nearby_ticket in nearby_tickets:
    for value in nearby_ticket:
        if not any([a <= value <= b for a, b in all_intervals]):
            error_rate += value
print(error_rate)