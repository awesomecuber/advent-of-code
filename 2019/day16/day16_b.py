import itertools
import operator
import os
import sys

with open(os.path.join(sys.path[0], "day16.txt")) as f:
    puzzle_input = f.read()
puzzle_input = '80871224585914546619083218645595'
nums = [int(n) for n in puzzle_input]

def ones_digit(num: int) -> int:
    return abs(num) % 10

# multiply input list by pattern (a dot product kinda)
def input_times_pattern(input: list[int], pattern: list[int]) -> int:
    return ones_digit(sum(map(operator.mul, input, itertools.cycle(pattern))))

def get_pattern(n):
    to_return = [0] * (n-1) + [1] * n + [0] * n + [-1] * n + [0]
    return to_return

def apply_phase(input_signal: list[int]):
    digits = [input_times_pattern(input_signal, get_pattern(n)) for n in range(1, len(input_signal) + 1)]
    return digits

for _ in range(100):
    nums = apply_phase(nums)
print(''.join(map(str, nums)))