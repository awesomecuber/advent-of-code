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
while player1_score < 1000 and player2_score < 1000:
    move_amount = 0
    for _ in range(3):
        dice_roll = (dice_roll % 100) + 1
        move_amount += dice_roll
        num_dice_rolled += 1
    player1_pos = (player1_pos + move_amount - 1) % 10 + 1
    player1_score += player1_pos
    if player1_score >= 1000:
        break

    move_amount = 0
    for _ in range(3):
        dice_roll = (dice_roll % 100) + 1
        move_amount += dice_roll
        num_dice_rolled += 1
    player2_pos = (player2_pos + move_amount - 1) % 10 + 1
    # 8 + 15
    player2_score += player2_pos

if player1_score < 1000:
    print(player1_score * num_dice_rolled)
if player2_score < 1000:
    print(player2_score * num_dice_rolled)
