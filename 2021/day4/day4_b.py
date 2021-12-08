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

losing_board = []
last_drawn = -1

for drawn in draw_numbers:
    delete_board_indexes = []
    for board_i, board in enumerate(boards):
        for i, row in enumerate(board):
            for j, num in enumerate(row):
                if num == drawn:
                    board[i][j] = -1
            if max(row) == -1:
                delete_board_indexes.append(board_i)
        for col in zip(*board):
            if max(col) == -1:
                delete_board_indexes.append(board_i)
    for i in sorted(set(delete_board_indexes), reverse=True):
        if len(boards) == 1:
            losing_board = board
            last_drawn = drawn
        del boards[i]
    if len(boards) == 0:
        break

unmarked_total = 0
for row in losing_board:
    for num in row:
        if num != -1:
            unmarked_total += num

print(unmarked_total * last_drawn)