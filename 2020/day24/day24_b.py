import os
import sys

with open(os.path.join(sys.path[0], "day24.txt")) as f:
    instructions = f.read().splitlines()

black_tiles: set[tuple[int, int]] = set()

for instruction in instructions:
    coord = [0, 0]
    temp_instruction = instruction
    while len(temp_instruction) > 0:
        if temp_instruction[0] in ["n", "s"]:
            if temp_instruction[0] == "n":
                coord[1] += 1
            elif temp_instruction[0] == "s":
                coord[1] -= 1
            if temp_instruction[1] == "e":
                coord[0] += 1
            elif temp_instruction[1] == "w":
                coord[0] -= 1
            temp_instruction = temp_instruction[2:]
        else:
            if temp_instruction[0] == "e":
                coord[0] += 2
            elif temp_instruction[0] == "w":
                coord[0] -= 2
            temp_instruction = temp_instruction[1:]
    if tuple(coord) in black_tiles:
        black_tiles.remove(tuple(coord))
    else:
        black_tiles.add(tuple(coord))


def adjacent_coords(coord):
    x, y = coord
    return [
        (x + 1, y + 1),
        (x - 1, y + 1),
        (x + 1, y - 1),
        (x - 1, y - 1),
        (x + 2, y),
        (x - 2, y),
    ]


for _ in range(100):
    black_tiles_to_flip: set[tuple[int, int]] = set()
    white_tiles_to_check: set[tuple[int, int]] = set()
    for black_tile in black_tiles:
        surrounding_black_tiles = 0
        for coord in adjacent_coords(black_tile):
            if coord in black_tiles:
                surrounding_black_tiles += 1
            else:
                white_tiles_to_check.add(coord)
        if surrounding_black_tiles == 0 or surrounding_black_tiles > 2:
            black_tiles_to_flip.add(black_tile)

    white_tiles_to_flip: set[tuple[int, int]] = set()
    for white_tile in white_tiles_to_check:
        surrounding_black_tiles = 0
        for coord in adjacent_coords(white_tile):
            if coord in black_tiles:
                surrounding_black_tiles += 1
        if surrounding_black_tiles == 2:
            white_tiles_to_flip.add(white_tile)

    black_tiles -= black_tiles_to_flip
    black_tiles |= white_tiles_to_flip
    print(len(black_tiles))
