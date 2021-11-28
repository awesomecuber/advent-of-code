import os
import sys

with open(os.path.join(sys.path[0], "day25.txt")) as f:
    puzzle_input = f.read().splitlines()

public_key1 = int(puzzle_input[0])
public_key2 = int(puzzle_input[1])

subject_number = 7
loop_size_1 = -1
loop_size_2 = -1
value = 1
i = 0
while loop_size_1 == -1 or loop_size_2 == -1:
    if value == public_key1:
        loop_size_1 = i
    if value == public_key2:
        loop_size_2 = i
    value = (value * 7) % 20201227
    i += 1

key = 1
for i in range(loop_size_1):
    key = (key * public_key2) % 20201227

print(key)