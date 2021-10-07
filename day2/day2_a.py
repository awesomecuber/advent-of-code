import re

with open("day2.txt") as f:
    puzzle_input = f.read().splitlines()

count = 0

for line in puzzle_input:
    items = re.split("-| |: ", line)
    min_count = int(items[0])
    max_count = int(items[1])
    character = items[2]
    password = items[3]
    character_count = password.count(character)
    if min_count <=  character_count <= max_count:
        count += 1

print(count)
