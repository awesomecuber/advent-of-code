import os
import sys

with open(os.path.join(sys.path[0], "day6.txt")) as f:
    puzzle_input = f.read().splitlines()

yes_questions = ""
group_size = 0
total_sum = 0
for line in puzzle_input + [""]:
    if line != "":
        yes_questions += line
        group_size += 1
    else:
        for question in set(yes_questions):
            if yes_questions.count(question) == group_size:
                total_sum += 1
        yes_questions = ""
        group_size = 0
print(total_sum)
