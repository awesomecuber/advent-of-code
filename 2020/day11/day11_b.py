import copy
import os
import sys

with open(os.path.join(sys.path[0], "day11.txt")) as f:
    puzzle_input = f.read().splitlines()

current_state = [list(x) for x in puzzle_input]
last_state = []

def print_state():
    for line in current_state:
        print(line)
    print()

while current_state != last_state:
    last_state = copy.deepcopy(current_state)
    for y, line in enumerate(last_state):
        for x, spot in enumerate(line):
            visible_occupied_seats = 0
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for direction in directions:
                x_eye = x
                y_eye = y
                while (0 <= x_eye + direction[0] <= len(line) - 1 and
                       0 <= y_eye + direction[1] <= len(last_state) - 1):
                    x_eye += direction[0]
                    y_eye += direction[1]
                    if last_state[y_eye][x_eye] == "L":
                        break
                    if last_state[y_eye][x_eye] == "#":
                        visible_occupied_seats += 1
                        break
            if spot == "L" and visible_occupied_seats == 0:
                current_state[y][x] = "#"
            if spot == "#" and visible_occupied_seats >= 5:
                current_state[y][x] = "L"

occupied_seat_count = 0
for line in current_state:
    for spot in line:
        if spot == "#":
            occupied_seat_count += 1
print(occupied_seat_count)