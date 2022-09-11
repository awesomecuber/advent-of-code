import os
import sys

with open(os.path.join(sys.path[0], "day16.txt")) as f:
    puzzle_input = f.read().splitlines()

classes = {}  # maps class name to ((a, b), (a, b))
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
nearby_tickets = [
    [int(y) for y in x.split(",")] for x in puzzle_input[first_space + 5 :]
]

all_intervals = [y for x in classes for y in classes[x]]

valid_tickets = []
for nearby_ticket in nearby_tickets:
    if all(
        [any([a <= value <= b for a, b in all_intervals]) for value in nearby_ticket]
    ):
        valid_tickets.append(nearby_ticket)

possible_classes = [set() for x in classes]


def value_valid_for_class(value, class_name):
    interval_one = classes[class_name][0]
    interval_two = classes[class_name][1]
    return (
        interval_one[0] <= value <= interval_one[1]
        or interval_two[0] <= value <= interval_two[1]
    )


for class_name in classes:
    for value_index in range(len(my_ticket)):
        if all(
            [value_valid_for_class(x[value_index], class_name) for x in valid_tickets]
        ):
            possible_classes[value_index].add(class_name)


def print_solutions(output=["" for x in classes]):
    if all([x != "" for x in output]):
        print(output)
        output_number = 1
        for i, class_name in enumerate(output):
            if class_name.find("departure") != -1:
                output_number *= my_ticket[i]
        print(output_number)
    else:
        first_unassigned_index = output.index("")
        remaining_classes = set([x for x in output if output != ""])
        available_classes = possible_classes[first_unassigned_index] - remaining_classes
        for class_name in available_classes:
            output[first_unassigned_index] = class_name
            print_solutions(output)
            output[first_unassigned_index] = ""


print_solutions()
