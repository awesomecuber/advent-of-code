from itertools import product
import heapq
import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day15.txt")) as f:
    puzzle_input = f.read().splitlines()

tile = [list(map(int, list(line))) for line in puzzle_input]

TILE_WIDTH = len(puzzle_input[0])
TILE_HEIGHT = len(puzzle_input)

WIDTH = TILE_WIDTH * 5
HEIGHT = TILE_HEIGHT * 5

risk_levels = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
for i, j in product(range(5), repeat=2):
    for x, y in product(range(TILE_WIDTH), range(TILE_HEIGHT)):
        value = (tile[y][x] + i + j) % 10
        if tile[y][x] + i + j >= 10:
            value += 1
        risk_levels[y + i * TILE_WIDTH][x + j * TILE_HEIGHT] = value

dists = [[-1 for _ in range(WIDTH)] for _ in range(HEIGHT)]
dists[0][0] = 0

visited: set[tuple[int, int]] = set()

to_visit: list[tuple[int, tuple[int, int]]] = [(0, (0, 0))]

def get_unvisited_neighbors(coord: tuple[int, int]):
    to_return = []
    x, y = coord
    shifts = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for shift_x, shift_y in shifts:
        new_x = x + shift_x
        new_y = y + shift_y
        if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT and (new_x, new_y) not in visited:
            to_return.append((new_x, new_y))
    return to_return

while len(to_visit) > 0:
    cur_dist, (x, y) = heapq.heappop(to_visit)

    if dists[y][x] != cur_dist:
        continue # we already found a better dist

    for next_x, next_y in get_unvisited_neighbors((x, y)):
        old_dist = dists[next_y][next_x]
        new_dist = cur_dist + risk_levels[next_y][next_x]
        if old_dist == -1 or new_dist < old_dist:
            dists[next_y][next_x] = new_dist
            heapq.heappush(to_visit, (new_dist, (next_x, next_y)))

    visited.add((x, y))

print(dists[HEIGHT - 1][WIDTH - 1])