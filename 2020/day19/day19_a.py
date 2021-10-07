import itertools
import os
import sys

with open(os.path.join(sys.path[0], "day19.txt")) as f:
    puzzle_input = f.read().splitlines()

break_index = puzzle_input.index("")
rules_input = puzzle_input[:break_index]
patterns = puzzle_input[break_index + 1:]

rules = {} #
for rule_input in rules_input:
    first_split = rule_input.split(": ")
    rule_num = int(first_split[0])
    if first_split[1].find("\"") != -1:
        rules[rule_num] = first_split[1][1]
    else:
        second_split = first_split[1].split(" | ")
        rules[rule_num] = [[int(y) for y in x.split(" ")] for x in second_split]

def generate_valid_patterns(rule_num):
    if isinstance(rules[rule_num], str):
        return {rules[rule_num]}
    toReturn = set()
    for pattern in rules[rule_num]:
        each_part = [generate_valid_patterns(y) for y in pattern]
        toReturn |= set((["".join(x) for x in itertools.product(*each_part)]))
    return toReturn

possible_patterns = generate_valid_patterns(0)

valid_patterns_count = 0
for pattern in patterns:
    if pattern in possible_patterns:
        valid_patterns_count += 1

print(valid_patterns_count)
# print(generate_valid_patterns(11))