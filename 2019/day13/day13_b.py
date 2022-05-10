import os
import sys

from intcode import ExitCode, IntCodeProgram

TILE_REPR = {
    0: ' ',
    1: '#',
    2: 'B',
    3: '_',
    4: 'o'
}

WIDTH = 37
HEIGHT = 20

MANUAL = False

Screen = dict[tuple[int, int], int]

with open(os.path.join(sys.path[0], "day13.txt")) as f:
    puzzle_input = f.read()

memory = [int(num) for num in puzzle_input.split(',')]
memory[0] = 2
arcade = IntCodeProgram(memory)

def update_screen(screen: Screen) -> int:
    global score
    while True:
        tile, exit_code = arcade.get_n_outputs(3)
        if exit_code in [ExitCode.NEED_INPUT, ExitCode.TERMINATE]:
            return exit_code

        x, y, type = tile
        if x == -1:
            score = type
        screen[x, y] = type

def print_screen(screen: Screen, score):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            print(TILE_REPR[screen[x,y]], end='')
        print()
    print(f'SCORE: {score}')

def get_paddle_position(screen: Screen):
    for coord, type in screen.items():
        if type == 3:
            return coord

def get_ball_position(screen: Screen):
    for coord, type in screen.items():
        if type == 4:
            return coord


screen: Screen = {}
score = 0
while True:
    exit_code = update_screen(screen)
    if exit_code == ExitCode.TERMINATE:
        break

    if MANUAL:
        print_screen(screen, score)
        move = input('(l)eft/(r)ight? (press enter for no action): ')
        if move == 'l':
            arcade.add_input(-1)
        elif move == 'r':
            arcade.add_input(1)
        else:
            arcade.add_input(0)
    else:
        paddle_x, _ = get_paddle_position(screen)
        ball_x, _ = get_ball_position(screen)
        if ball_x < paddle_x:
            arcade.add_input(-1)
        elif ball_x > paddle_x:
            arcade.add_input(1)
        else:
            arcade.add_input(0)

print(score)