from collections import defaultdict
from functools import cache
import os
import sys

with open(os.path.join(sys.path[0], "day6.txt")) as f:
    puzzle_input = f.read().splitlines()

# dict from object to what it orbits
objects: dict[str, str] = defaultdict(str)

for line in puzzle_input:
    center, orbiter = line.split(")")
    objects[orbiter] = center


@cache
def get_num_orbits(object):
    if object not in objects:
        return 0
    return get_num_orbits(objects[object]) + 1


total_answer = 0
for object in objects:
    total_answer += get_num_orbits(object)
print(total_answer)
