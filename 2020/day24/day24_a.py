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
print(len(black_tiles))
