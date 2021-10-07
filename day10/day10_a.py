with open("day10.txt") as f:
    puzzle_input = f.read().splitlines()
    
puzzle_nums = sorted([int(x) for x in puzzle_input])
puzzle_nums = [0] + puzzle_nums + [puzzle_nums[-1] + 3]
print(puzzle_nums)

one_diff = 0
three_diff = 0
for i in range(len(puzzle_nums) - 1):
    diff = puzzle_nums[i + 1] - puzzle_nums[i]
    if diff == 1:
        one_diff += 1
    elif diff == 3:
        three_diff += 1
print(one_diff * three_diff)