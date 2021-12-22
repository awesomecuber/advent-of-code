from functools import cache
import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day21.txt")) as f:
    puzzle_input = f.read().splitlines()

player1_pos = int(puzzle_input[0][-1])
player2_pos = int(puzzle_input[1][-1])

player1_score = 0
player2_score = 0

num_dice_rolled = 0

dice_roll = 0

map = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
}

@cache
def num_win_universes(p1_pos, p1_score, p2_pos, p2_score, turn):
    if p1_score >= 21:
        return 1, 0
    if p2_score >= 21:
        return 0, 1
    if turn == 1:
        p1_win_universes, p2_win_universes = 0, 0
        for increment, times in map.items():
            new_p1_pos = (p1_pos + increment - 1) % 10 + 1
            new_p1_win_universes, new_p2_win_universes = num_win_universes(
                new_p1_pos,
                p1_score + new_p1_pos,
                p2_pos,
                p2_score,
                2
            )
            p1_win_universes += times * new_p1_win_universes
            p2_win_universes += times * new_p2_win_universes
        return p1_win_universes, p2_win_universes
    if turn == 2:
        p1_win_universes, p2_win_universes = 0, 0
        for increment, times in map.items():
            new_p2_pos = (p2_pos + increment - 1) % 10 + 1
            new_p1_win_universes, new_p2_win_universes = num_win_universes(
                p1_pos,
                p1_score,
                new_p2_pos,
                p2_score + new_p2_pos,
                1
            )
            p1_win_universes += times * new_p1_win_universes
            p2_win_universes += times * new_p2_win_universes
        return p1_win_universes, p2_win_universes

p1_universes, p2_universes = num_win_universes(
    player1_pos,
    player1_score,
    player2_pos,
    player2_score,
    1
)

print(max(p1_universes, p2_universes))