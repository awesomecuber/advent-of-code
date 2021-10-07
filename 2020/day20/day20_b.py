from copy import deepcopy
from itertools import product
import math
import os
import sys

with open(os.path.join(sys.path[0], "day20ex.txt")) as f:
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

def convert_tile(tile_id, orientation):
    tile_content = deepcopy(tiles[tile_id])
    if orientation >= 4:
        tile_content = ["".join(reversed(x)) for x in tile_content]
    rotation = orientation % 4
    for i in range(rotation):
        tile_content = ["".join(reversed(list(x))) for x in zip(*tile_content)]
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
    cut_tiles = deepcopy(tiles)
    for right_tile in [x for x in board if x[0] > 0]:
        tile_id = board[right_tile]
        print(tile_id)
        # convert_tile(*board[right_tile])
        # cut_tiles[]

board = fill_board()
print(board)
print("found tiling")
form_picture(board)