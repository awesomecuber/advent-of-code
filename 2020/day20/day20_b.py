from copy import deepcopy
from itertools import product
import math
import os
import sys

with open(os.path.join(sys.path[0], "day20.txt")) as f:
    puzzle_input = f.read().splitlines()

tiles = {}
while len(puzzle_input) > 1:
    tile_input = puzzle_input[:11]
    tiles[int(tile_input[0][5:-1])] = tile_input[1:]
    puzzle_input = puzzle_input[12:]

board_size = int(math.sqrt(len(tiles)))

# orientation: 0 1 2 3 4 5 6 7
# 0-3 are unflipped, 4-7 are flipped (horizontally)
# %0 is normal, %1 is clockwise, %2 is 180, %3 is counterclockwise

def get_nearby_coordinates(current):
    current_coords = current.keys()
    to_return = set()
    for current_coord in current_coords:
        coords_to_check = [
            (current_coord[0] + 1, current_coord[1]),
            (current_coord[0] - 1, current_coord[1]),
            (current_coord[0], current_coord[1] + 1),
            (current_coord[0], current_coord[1] - 1)
        ]
        for coord in coords_to_check:
            if coord not in current:
                to_return.add(coord)
    # trim if width is equal to board_size
    all_x = [x[0] for x in current_coords]
    all_y = [x[1] for x in current_coords]

    if max(all_x) - min(all_x) == board_size - 1:
        to_return = [x for x in to_return if min(all_x) <= x[0] <= max(all_x)]
    if max(all_y) - min(all_y) == board_size - 1:
        to_return = [x for x in to_return if min(all_y) <= x[1] <= max(all_y)]
    return to_return

def convert_tile(tile_id, orientation, cut=False):
    tile_content = deepcopy(tiles[tile_id])
    if orientation >= 4:
        tile_content = ["".join(reversed(x)) for x in tile_content]
    rotation = orientation % 4
    for i in range(rotation):
        tile_content = ["".join(reversed(list(x))) for x in zip(*tile_content)]
    if cut:
        tile_content = [line[1:-1] for line in tile_content[1:-1]]
    return tile_content

def left(tile_id, orientation):
    tile_content = convert_tile(tile_id, orientation)
    return "".join([x[0] for x in tile_content])

def right(tile_id, orientation):
    tile_content = convert_tile(tile_id, orientation)
    return "".join([x[len(x) - 1] for x in tile_content])

def top(tile_id, orientation):
    tile_content = convert_tile(tile_id, orientation)
    return tile_content[0]

def bottom(tile_id, orientation):
    tile_content = convert_tile(tile_id, orientation)
    return tile_content[len(tile_content) - 1]

def fill_board(current={}):
    if current == {}:
        current[(0, 0)] = (next(iter(tiles)), 6)
    if len(current) == board_size ** 2:
        return current
    remaining_tile_ids = tiles.keys() - [x[0] for x in current.values()]
    nearby_coords = get_nearby_coordinates(current)
    for coord, tile_id, orientation in product(nearby_coords, remaining_tile_ids, range(8)):
        left_coord = (coord[0] - 1, coord[1])
        right_coord = (coord[0] + 1, coord[1])
        top_coord = (coord[0], coord[1] + 1)
        bottom_coord = (coord[0], coord[1] - 1)

        if (
            (left_coord not in current or left(tile_id, orientation) == right(*current[left_coord])) and
            (right_coord not in current or right(tile_id, orientation) == left(*current[right_coord])) and
            (top_coord not in current or top(tile_id, orientation) == bottom(*current[top_coord])) and
            (bottom_coord not in current or bottom(tile_id, orientation) == top(*current[bottom_coord]))
        ):
            current[coord] = (tile_id, orientation)
            result = fill_board(current)
            if result != {}:
                return result
            del current[coord]
    return {}


def form_picture(board):
    to_return = []

    min_x = min([tile_coord[0] for tile_coord in board])
    max_x = max([tile_coord[0] for tile_coord in board])
    min_y = min([tile_coord[1] for tile_coord in board])
    max_y = max([tile_coord[1] for tile_coord in board])
    tile_size = len(tiles[board[(min_x, min_y)][0]][0]) - 2

    for row_num, y in enumerate(range(max_y, min_y - 1, -1)):
        to_return += ['' for _ in range(tile_size)]
        for x in range(min_x, max_x + 1):
            for i, line in enumerate(convert_tile(*board[(x, y)], True)):
                to_return[i + row_num * tile_size] += line
    return to_return

board = fill_board()
print(board)
print("found tiling")
picture = form_picture(board)

base_sea_monster = ['                  # ',
                    '#    ##    ##    ###',
                    ' #  #  #  #  #  #   ']

all_sea_monsters = []

for _ in range(4):
    all_sea_monsters.append(base_sea_monster)
    base_sea_monster = ["".join(reversed(list(x))) for x in zip(*base_sea_monster)]
base_sea_monster = ["".join(reversed(x)) for x in base_sea_monster]
for _ in range(4):
    all_sea_monsters.append(base_sea_monster)
    base_sea_monster = ["".join(reversed(list(x))) for x in zip(*base_sea_monster)]

num_monsters = 0
for sea_monster in all_sea_monsters:
    for y in range(0, len(picture) - len(sea_monster)):
        for x in range(0, len(picture[0]) - len(sea_monster[0])):
            found_monster = True
            for (monster_y, row) in enumerate(sea_monster):
                for (monster_x, char) in enumerate(row):
                    if char == '#' and picture[y + monster_y][x + monster_x] not in ['#', 'o']:
                        found_monster = False
            if found_monster:
                num_monsters += 1
                for (monster_y, row) in enumerate(sea_monster):
                    for (monster_x, char) in enumerate(row):
                        if char == '#':
                            list_of_row = list(picture[y + monster_y])
                            list_of_row[x + monster_x] = 'o'
                            picture[y + monster_y] = ''.join(list_of_row)

roughness = 0
for row in picture:
    for char in row:
        if char == '#':
            roughness += 1
print('roughness: ', roughness)