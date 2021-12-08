import pprint

import os
import sys

with open(os.path.join(sys.path[0], "day4.txt")) as f:
    puzzle_input = f.read().splitlines()

draw_numbers = [int(x) for x in puzzle_input[0].split(',')]
puzzle_input = puzzle_input[2:]

boards = []

while len(puzzle_input) != 0:
    new_board = []
    for row in puzzle_input[:5]:
        new_board.append([int(x) for x in row.split()])
    boards.append(new_board)
    puzzle_input = puzzle_input[6:]

winning_board = []
last_drawn = -1

for drawn in draw_numbers:
    for board in boards:
        for i, row in enumerate(board):
            for j, num in enumerate(row):
                if num == drawn:
                    board[i][j] = -1
            if max(row) == -1:
                winning_board = board
                last_drawn = drawn
        for col in zip(*board):
            if max(col) == -1:
                winning_board = board
                last_drawn = drawn
    if winning_board != []:
        break

unmarked_total = 0
for row in winning_board:
    for num in row:
        if num != -1:
            unmarked_total += num

print(unmarked_total * last_drawn)