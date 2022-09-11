import collections
import os
import sys

with open(os.path.join(sys.path[0], "day22.txt")) as f:
    puzzle_input = f.read().splitlines()

divider = puzzle_input.index("")
cards1 = puzzle_input[1:divider]
cards2 = puzzle_input[divider + 2 :]

player1start = collections.deque(int(card) for card in cards1)
player2start = collections.deque(int(card) for card in cards2)


def play_game(player1, player2):
    all_rounds = set()
    while len(player1) > 0 and len(player2) > 0:
        hashable_cards = (tuple(player1), tuple(player2))
        if hashable_cards in all_rounds:
            break  # player 1 wins the game
        all_rounds.add(hashable_cards)

        player1top = player1.popleft()
        player2top = player2.popleft()

        player1wins = False
        if player1top <= len(player1) and player2top <= len(player2):
            player1subhand = collections.deque(list(player1)[:player1top])
            player2subhand = collections.deque(list(player2)[:player2top])
            player1end, _ = play_game(player1subhand, player2subhand)
            player1wins = len(player1end) > 0
        else:
            player1wins = player1top > player2top

        if player1wins:
            player1.append(player1top)
            player1.append(player2top)
        else:
            player2.append(player2top)
            player2.append(player1top)
    return player1, player2


player1end, player2end = play_game(player1start, player2start)


def calculate_score(hand):
    return sum([i * card for i, card in enumerate(reversed(hand), start=1)])


if (
    len(player1end) > 0
):  # either player2 has no cards or game ended early with duplicate
    print("player 1 wins!")
    print(calculate_score(player1end))
else:
    print("player 2 wins!")
    print(calculate_score(player2end))
