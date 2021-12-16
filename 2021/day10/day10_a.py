import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day10.txt")) as f:
    puzzle_input = f.read().splitlines()

error_score = 0
for line in puzzle_input:
    opened = []
    for char in line:
        if char in ['(', '[', '{', '<']:
            opened.append(char)
        if char == ')' and opened.pop() != '(':
            error_score += 3
            break
        if char == ']' and opened.pop() != '[':
            error_score += 57
            break
        if char == '}' and opened.pop() != '{':
            error_score += 1197
            break
        if char == '>' and opened.pop() != '<':
            error_score += 25137
            break

print(error_score)