from itertools import cycle
from math import atan2, gcd, pi
import os
import sys

with open(os.path.join(sys.path[0], "day10.txt")) as f:
    puzzle_input = f.read().splitlines()

asteroids = set()

for y, line in enumerate(puzzle_input):
    for x, char in enumerate(line):
        if char == "#":
            asteroids.add((x, y))


def get_dir(monitering_station, other_asteroid):
    if monitering_station == other_asteroid:
        raise Exception("monitering and other must be different")

    station_x, station_y = monitering_station
    other_x, other_y = other_asteroid

    diff_x = other_x - station_x
    diff_y = other_y - station_y

    dist = gcd(diff_x, diff_y)
    dir_x = int(diff_x / dist)
    dir_y = int(diff_y / dist)

    return dir_x, dir_y


def asteroid_visible(monitering_station, other_asteroid):
    if monitering_station == other_asteroid:
        return False

    station_x, station_y = monitering_station
    other_x, other_y = other_asteroid

    dir_x, dir_y = get_dir(monitering_station, other_asteroid)

    cur_spot_x = station_x + dir_x
    cur_spot_y = station_y + dir_y
    while (cur_spot_x, cur_spot_y) != (other_x, other_y):
        if (cur_spot_x, cur_spot_y) in asteroids:
            return False
        cur_spot_x += dir_x
        cur_spot_y += dir_y
    return True


most_visible = -1
station_location = None

for monitering_station in asteroids:
    visible_asteroids = 0
    for other_asteroid in asteroids:
        if asteroid_visible(monitering_station, other_asteroid):
            visible_asteroids += 1
    if visible_asteroids > most_visible:
        most_visible = visible_asteroids
        station_location = monitering_station

# we now know where the station goes

asteroids.remove(station_location)  # type: ignore

all_dirs = set()
for asteroid in asteroids:
    all_dirs.add(get_dir(station_location, asteroid))


def get_angle(dir):
    angle = atan2(dir[0], -dir[1])
    if angle < 0:
        angle += 2 * pi
    return angle


sorted_dirs = sorted(all_dirs, key=get_angle)

MAX_X = max(x for x, _ in asteroids)
MAX_Y = max(y for _, y in asteroids)


def vaporize_asteroid(dir):
    cur_x = station_location[0] + dir[0]
    cur_y = station_location[1] + dir[1]

    while (cur_x, cur_y) not in asteroids:
        cur_x += dir[0]
        cur_y += dir[1]
        if not (0 <= cur_x <= MAX_X and 0 <= cur_y <= MAX_Y):
            return None

    asteroids.remove((cur_x, cur_y))
    return cur_x, cur_y


vaporized_count = 0
for dir in cycle(sorted_dirs):
    asteroid_vaporized = vaporize_asteroid(dir)
    if asteroid_vaporized is None:
        sorted_dirs.remove(dir)
    else:
        vaporized_count += 1
        if vaporized_count == 200:
            print(asteroid_vaporized[0] * 100 + asteroid_vaporized[1])
            break
