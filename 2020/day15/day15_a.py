puzzle_input = "2,0,6,12,1,3"
nums = [int(x) for x in puzzle_input.split(",")]

previous_nums = {} # maps the value of the number to the turn where that number was last

for i, num in enumerate(nums[:-1]):
    previous_nums[num] = i + 1

for turn in range(len(nums) + 1, 2021):
    last_num = nums[len(nums) - 1]
    if last_num in previous_nums:
        new_num = turn - 1 - previous_nums[last_num]
    else:
        new_num = 0
    nums.append(new_num)
    previous_nums[last_num] = turn - 1

print(nums[len(nums) - 1])