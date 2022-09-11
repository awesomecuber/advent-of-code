from collections import defaultdict
import os
import sys

with open(os.path.join(sys.path[0], "day6.txt")) as f:
    puzzle_input = f.read().splitlines()

# dict from object to what it's connected to
objects: dict[str, str] = defaultdict(str)

for line in puzzle_input:
    center, orbiter = line.split(")")
    objects[orbiter] = center

you_path = []

cur_object = "YOU"
while cur_object in objects:
    cur_object = objects[cur_object]
    you_path.append(cur_object)

san_path = []

you_path_set = set(you_path)

cur_object = "SAN"
while cur_object not in you_path_set:
    cur_object = objects[cur_object]
    san_path.append(cur_object)

you_path_length = len(you_path[: you_path.index(cur_object)]) + 1
san_path_length = len(san_path)

print(san_path_length + you_path_length - 2)
