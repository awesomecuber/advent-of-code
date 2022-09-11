import os
import sys

with open(os.path.join(sys.path[0], "day16.txt")) as f:
    puzzle_input = f.read()

nums = [int(n) for n in puzzle_input] * 10000
message_offset = int(puzzle_input[:7])

for i in range(100):
    print(i)
    next_nums = nums.copy()
    total = 0
    for j in range(len(next_nums) - 1, message_offset - 1, -1):
        total += next_nums[j]
        next_nums[j] = abs(total) % 10  # ones digit
    nums = next_nums

print("".join(map(str, nums[message_offset : message_offset + 8])))
