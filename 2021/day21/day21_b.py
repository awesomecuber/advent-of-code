from functools import cache
import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day21ex.txt")) as f:
    puzzle_input = f.read().splitlines()

player1_pos = int(puzzle_input[0][-1])
player2_pos = int(puzzle_input[1][-1])

player1_score = 0
player2_score = 0

num_dice_rolled = 0

dice_roll = 0

@cache
def num_wins(p1_pos, p1_score, p2_pos, p2_score, turn):
    if p1_score >= 21:
        return 1, 0
    if p2_score >= 21:
        return 0, 1
    if turn == 1:
        new_p1_pos = (p1_pos % 10) + 1
        p1wins_1, p2wins_1 = num_wins(new_p1_pos, p1_score + new_p1_pos, p2_pos, p2_score, 2)
        new_p1_pos = (p1_pos % 10) + 1
        p1wins_2, p2wins_2 = num_wins(new_p1_pos, p1_score + new_p1_pos, p2_pos, p2_score, 2)
        new_p1_pos = (p1_pos % 10) + 1
        p1wins_3, p2wins_3 = num_wins(new_p1_pos, p1_score + new_p1_pos, p2_pos, p2_score, 2)
        return p1wins_1 + p1wins_2 + p1wins_3, p2wins_1 + p2wins_2 + p2wins_3
    if turn == 2:
        new_p2_pos = (p1_pos % 10) + 1
        p1wins_1, p2wins_1 = num_wins(p1_pos, p1_score, new_p2_pos, p2_score + new_p2_pos, 1)
        new_p2_pos = (p1_pos % 10) + 1
        p1wins_2, p2wins_2 = num_wins(p1_pos, p1_score, new_p2_pos, p2_score + new_p2_pos, 1)
        new_p2_pos = (p1_pos % 10) + 1
        p1wins_3, p2wins_3 = num_wins(p1_pos, p1_score, new_p2_pos, p2_score + new_p2_pos, 1)
        return p1wins_1 + p1wins_2 + p1wins_3, p2wins_1 + p2wins_2 + p2wins_3

print(num_wins(player1_pos, player1_score, player2_pos, player2_score, 1))