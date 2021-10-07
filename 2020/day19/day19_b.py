import itertools
import os
import sys

with open(os.path.join(sys.path[0], "day19.txt")) as f:
    puzzle_input = f.read().splitlines()

break_index = puzzle_input.index("")
rules_input = puzzle_input[:break_index]
patterns = puzzle_input[break_index + 1:]

rules = {}
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

fourty_two_patterns = generate_valid_patterns(42)
thirty_one_patterns = generate_valid_patterns(31)

fourty_two_length = len(next(iter(fourty_two_patterns)))
thirty_one_length = len(next(iter(thirty_one_patterns)))

# pattern is: 42 * n + 42 * m + 31 * m
valid_patterns_count = 0
for pattern in patterns:
    possible_counts = set()
    for n in range(1, len(pattern) // fourty_two_length):
        m = (len(pattern) - n * fourty_two_length) / (fourty_two_length + thirty_one_length)
        if m.is_integer():
            m = int(m)
            possible_counts.add((n, m))
    for n, m in possible_counts:
        fourty_two_partitions = [pattern[fourty_two_length * i:fourty_two_length * (i + 1)] for i in range(n + m)]
        thirty_one_partitions = [pattern[thirty_one_length * i:thirty_one_length * (i + 1)] for i in range(n + m, n + 2 * m)]
        if (
            all(x in fourty_two_patterns for x in fourty_two_partitions) and
            all(x in thirty_one_patterns for x in thirty_one_partitions)
        ):
            valid_patterns_count += 1
            break

print(valid_patterns_count)