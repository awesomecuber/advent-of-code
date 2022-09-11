import pprint
import os
import sys
from collections import Counter

with open(os.path.join(sys.path[0], "day14.txt")) as f:
    puzzle_input = f.read().splitlines()

template: str = puzzle_input[0]
insertion_rules: dict[str, str] = {}

for line in puzzle_input:
    insertion_rules[line[:2]] = line[-1:]

# .NNCB

# NCNCB to NCN B CB where i=2

# NC.NCB
# NCNB.CB
# NCNBCH.B

for _ in range(40):
    i = 0
    while i < len(template) - 1:
        if template[i : i + 2] in insertion_rules:
            template = (
                template[: i + 1]
                + insertion_rules[template[i : i + 2]]
                + template[i + 1 :]
            )
            i += 1
        i += 1

counter = Counter(template)
sorted_elements = sorted(counter.items(), key=lambda x: x[1])

print(sorted_elements[-1][1] - sorted_elements[0][1])
