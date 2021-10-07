import os
import sys

with open(os.path.join(sys.path[0], "day4.txt")) as f:
    puzzle_input = f.read().splitlines()

current_passport_fields = []
valid_count = 0
for line in puzzle_input + [""]:
    if line != "":
        fields = [field.split(":")[0] for field in line.split()]
        current_passport_fields += fields
    else:
        if len(set([field for field in current_passport_fields if field != "cid"])) == 7:
            valid_count += 1
        current_passport_fields = []
print(valid_count)