# from copy import deepcopy
from enum import Enum

# from pprint import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day25.txt")) as f:
    puzzle_input = f.read().splitlines()

# puzzle_input = ['v..', '>..']


class Spot(Enum):
    BLANK = 0
    RIGHT = 1
    DOWN = 2


WIDTH = len(puzzle_input[0])
HEIGHT = len(puzzle_input)

spots: list[list[Spot]] = []
for line in puzzle_input:
    spots_line: list[Spot] = []
    for char in line:
        match char:
            case ".":
                to_add = Spot.BLANK
            case ">":
                to_add = Spot.RIGHT
            case "v":
                to_add = Spot.DOWN
        spots_line.append(to_add)  # type: ignore
    spots.append(spots_line)


def print_board(spots: list[list[Spot]]):
    for line in spots:
        for spot in line:
            match spot:
                case Spot.BLANK:
                    print(".", end="")
                case Spot.RIGHT:
                    print(">", end="")
                case Spot.DOWN:
                    print("v", end="")
        print()


things_moving = True
step = 0
while things_moving:
    print(step)
    next_spots = [[Spot.BLANK for _ in range(WIDTH)] for _ in range(HEIGHT)]
    things_moving = False
    step += 1
    for y, line in enumerate(spots):
        for x, spot in enumerate(line):
            if spot == Spot.RIGHT:
                new_x = (x + 1) % WIDTH
                new_y = y
                if spots[new_y][new_x] == Spot.BLANK:
                    things_moving = True
                    next_spots[new_y][new_x] = spots[y][x]
                else:
                    next_spots[y][x] = spots[y][x]
            if spot == Spot.DOWN:
                next_spots[y][x] = spots[y][x]
    spots = next_spots

    next_spots = [[Spot.BLANK for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for y, line in enumerate(spots):
        for x, spot in enumerate(line):
            if spot == Spot.DOWN:
                new_x = x
                new_y = (y + 1) % HEIGHT
                if spots[new_y][new_x] == Spot.BLANK:
                    things_moving = True
                    next_spots[new_y][new_x] = spots[y][x]
                else:
                    next_spots[y][x] = spots[y][x]
            if spot == Spot.RIGHT:
                next_spots[y][x] = spots[y][x]

    spots = next_spots

print(step)
