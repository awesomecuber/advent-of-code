import re

with open("day2.txt") as f:
    puzzle_input = f.read().splitlines()

count = 0

for line in puzzle_input:
    items = re.split("-| |: ", line)
    first = int(items[0]) - 1
    second = int(items[1]) - 1
    character = items[2]
    password = items[3]
    if (password[first] == character) ^ (password[second] == character):
        count += 1

print(count)
