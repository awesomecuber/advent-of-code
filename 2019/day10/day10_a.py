from math import gcd
import os
import sys

with open(os.path.join(sys.path[0], "day10.txt")) as f:
    puzzle_input = f.read().splitlines()

asteroids = set()

for y, line in enumerate(puzzle_input):
    for x, char in enumerate(line):
        if char == "#":
            asteroids.add((x, y))


def asteroid_visible(monitering_station, other_asteroid):
    if monitering_station == other_asteroid:
        return False

    station_x, station_y = monitering_station
    other_x, other_y = other_asteroid

    diff_x = other_x - station_x
    diff_y = other_y - station_y

    dist = gcd(diff_x, diff_y)
    dir_x = int(diff_x / dist)
    dir_y = int(diff_y / dist)

    cur_spot_x = station_x + dir_x
    cur_spot_y = station_y + dir_y
    while (cur_spot_x, cur_spot_y) != (other_x, other_y):
        if (cur_spot_x, cur_spot_y) in asteroids:
            return False
        cur_spot_x += dir_x
        cur_spot_y += dir_y
    return True


most_visible = 0

for monitering_station in asteroids:
    visible_asteroids = 0
    for other_asteroid in asteroids:
        if asteroid_visible(monitering_station, other_asteroid):
            visible_asteroids += 1
    most_visible = max(most_visible, visible_asteroids)

print(most_visible)
