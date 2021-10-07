with open("day1.txt") as f:
    puzzle_input = f.read().splitlines()
puzzle_nums = [int(line) for line in puzzle_input]
nums_set = set(puzzle_nums)

for num in puzzle_nums:
    if (2020 - num) in nums_set:
        print((2020 - num) * num)
