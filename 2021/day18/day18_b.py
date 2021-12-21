from __future__ import annotations

import copy
from dataclasses import dataclass
from itertools import permutations
import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day18.txt")) as f:
    puzzle_input = f.read().splitlines()

class Number:
    def __init__(self, line):
        self.left_child: Number = None
        self.right_child: Number = None
        self.val: int = -1

        if line[0] == '[':
            line = line[1:-1]

            i = 0
            bracket_count = 0
            while i == 0 or bracket_count > 0:
                if line[i] == '[':
                    bracket_count += 1
                if line[i] == ']':
                    bracket_count -= 1
                i += 1
            left_line = line[:i]
            right_line = line[i+1:]

            self.left_child = Number(left_line)
            self.right_child = Number(right_line)
        else:
            self.val = int(line)

    def __add__(self, other):
        to_return = Number('-1')
        to_return.left_child = copy.deepcopy(self)
        to_return.right_child = copy.deepcopy(other)
        while True:
            leaves = to_return.get_leaves()
            exploding_pair = to_return.find_exploding_pair()
            if exploding_pair is not None:
                first_i = leaves.index(exploding_pair.left_child)
                if first_i > 0:
                    leaves[first_i - 1].val += leaves[first_i].val
                if first_i < len(leaves) - 2:
                    leaves[first_i + 2].val += leaves[first_i + 1].val
                exploding_pair.left_child = None
                exploding_pair.right_child = None
                exploding_pair.val = 0

                continue

            first_leaf_to_split = None
            for leaf in leaves:
                if leaf.val > 9:
                    first_leaf_to_split = leaf
                    break
            if first_leaf_to_split is not None:
                left_num = first_leaf_to_split.val // 2
                right_num = first_leaf_to_split.val // 2
                if first_leaf_to_split.val % 2 == 1:
                    right_num += 1
                first_leaf_to_split.left_child = Number(str(left_num))
                first_leaf_to_split.right_child = Number(str(right_num))
                first_leaf_to_split.val = -1

                continue

            break

        return to_return

    def find_exploding_pair(self, level=0):
        if level == 4 and self.val == -1:
            return self
        if self.val != -1:
            return None
        left_exploding_pair = self.left_child.find_exploding_pair(level+1)
        if left_exploding_pair is not None:
            return left_exploding_pair
        right_exploding_pair = self.right_child.find_exploding_pair(level+1)
        if right_exploding_pair is not None:
            return right_exploding_pair
        return None

    def split(self):
        pass

    def get_leaves(self):
        if self.val != -1:
            return [self]
        left_leaves = self.left_child.get_leaves()
        right_leaves = self.right_child.get_leaves()
        return left_leaves + right_leaves

    def magnitude(self):
        if self.val != -1:
            return self.val
        return 3 * self.left_child.magnitude() + 2* self.right_child.magnitude()

    def __str__(self):
        if self.val != -1:
            return str(self.val)
        return f'[{self.left_child},{self.right_child}]'

max_magnitude = 0
numbers = [Number(line) for line in puzzle_input]
for num1, num2 in permutations(numbers, 2):
    new_magnitude = (num1 + num2).magnitude()
    max_magnitude = max(max_magnitude, new_magnitude)

print(max_magnitude)
