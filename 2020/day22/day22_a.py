import collections
import os
import sys

with open(os.path.join(sys.path[0], "day22.txt")) as f:
    puzzle_input = f.read().splitlines()

divider = puzzle_input.index('')
cards1 = puzzle_input[1:divider]
cards2 = puzzle_input[divider+2:]

player1 = collections.deque(int(card) for card in cards1)
player2 = collections.deque(int(card) for card in cards2)

while len(player1) > 0 and len(player2) > 0:
    player1top = player1.popleft()
    player2top = player2.popleft()
    if player1top > player2top:
        player1.append(player1top)
        player1.append(player2top)
    else:
        player2.append(player2top)
        player2.append(player1top)

if len(player1) > 0:
    print('player 1 wins!')
    print(sum([i * card for i, card in enumerate(reversed(player1), start=1)]))
else:
    print('player 2 wins!')
    print(sum([i * card for i, card in enumerate(reversed(player2), start=1)]))