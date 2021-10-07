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
            adjacent_occupied_seats = 0
            if x > 0:
                if last_state[y][x - 1] == "#":
                    adjacent_occupied_seats += 1
                if y > 0 and last_state[y - 1][x - 1] == "#":
                    adjacent_occupied_seats += 1
                if y < len(last_state) - 1 and last_state[y + 1][x - 1] == "#":
                    adjacent_occupied_seats += 1
            if x < len(line) - 1:
                if last_state[y][x + 1] == "#":
                    adjacent_occupied_seats += 1
                if y > 0 and last_state[y - 1][x + 1] == "#":
                    adjacent_occupied_seats += 1
                if y < len(last_state) - 1 and last_state[y + 1][x + 1] == "#":
                    adjacent_occupied_seats += 1
            if y > 0 and last_state[y - 1][x] == "#":
                adjacent_occupied_seats += 1
            if y < len(last_state) - 1 and last_state[y + 1][x] == "#":
                adjacent_occupied_seats += 1
            if spot == "L" and adjacent_occupied_seats == 0:
                current_state[y][x] = "#"
            if spot == "#" and adjacent_occupied_seats >= 4:
                current_state[y][x] = "L"

occupied_seat_count = 0
for line in current_state:
    for spot in line:
        if spot == "#":
            occupied_seat_count += 1
print(occupied_seat_count)