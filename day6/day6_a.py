with open("day6.txt") as f:
    puzzle_input = f.read().splitlines()

yes_questions = []
total_sum = 0
for line in puzzle_input + [""]:
    if line != "":
        yes_questions += line
    else:
        total_sum += len(set(yes_questions))
        yes_questions = []
print(total_sum)