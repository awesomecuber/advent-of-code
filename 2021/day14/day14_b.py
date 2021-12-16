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

pairs: Counter[str] = Counter()

for letter1, letter2 in zip(template, template[1:]):
    pairs[letter1 + letter2] += 1

for _ in range(40):
    new_pairs: Counter[str] = Counter()
    for pair, count in pairs.items():
        if pair in insertion_rules:
            new_pairs[pair[0] + insertion_rules[pair]] += count
            new_pairs[insertion_rules[pair] + pair[1]] += count
    pairs = new_pairs

letter_count: Counter[str] = Counter()
for pair, count in pairs.items():
    letter_count[pair[0]] += count
    letter_count[pair[1]] += count

# make sure first and last letters are also double counted
letter_count[template[0]] += 1
letter_count[template[-1]] += 1

for letter, count in letter_count.items():
    letter_count[letter] //= 2

sorted_letter_count = letter_count.most_common()
print(sorted_letter_count[0][1] - sorted_letter_count[-1][1])