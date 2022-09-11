def solve(nums):
    if len(nums) == 2:
        return 1
    to_return = 0
    for i in range(1, len(nums)):
        if nums[i] - nums[0] <= 3:
            to_return += solve(nums[i:])
        else:
            break
    return to_return


print(solve([0, 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, 22]))
