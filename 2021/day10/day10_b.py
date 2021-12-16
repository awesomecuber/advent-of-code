import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day10.txt")) as f:
    puzzle_input = f.read().splitlines()

scores = []
for line in puzzle_input:
    opened = []
    incomplete = True
    for char in line:
        if char in ['(', '[', '{', '<']:
            opened.append(char)
        if char == ')' and opened.pop() != '(':
            incomplete = False
            break
        if char == ']' and opened.pop() != '[':
            incomplete = False
            break
        if char == '}' and opened.pop() != '{':
            incomplete = False
            break
        if char == '>' and opened.pop() != '<':
            incomplete = False
            break
    if incomplete:
        score = 0
        for open_char in reversed(opened):
            score *= 5
            if open_char == '(':
                score += 1
            if open_char == '[':
                score += 2
            if open_char == '{':
                score += 3
            if open_char == '<':
                score += 4
        scores.append(score)

print(sorted(scores)[len(scores) // 2])