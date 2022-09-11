import os
import sys

with open(os.path.join(sys.path[0], "day7.txt")) as f:
    puzzle_input = f.read().splitlines()

bags = {}

for line in puzzle_input:
    split = line.split(" contain ")
    bag_color = split[0][:-5]
    if split[1] == "no other bags.":
        bags[bag_color] = []
    else:
        bags[bag_color] = [x[2 : x.index(" bag")] for x in split[1].split(", ")]


def bag_has_color(bag, color):
    sub_colors = bags[bag]
    if color in sub_colors:
        return True
    elif len(sub_colors) == 0:
        return False

    return any([bag_has_color(sub_color, color) for sub_color in sub_colors])


total_count = 0
for color in bags:
    if bag_has_color(color, "shiny gold"):
        total_count += 1
print(total_count)
