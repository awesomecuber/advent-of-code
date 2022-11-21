from pprint import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day24.txt")) as f:
    puzzle_input = f.read().splitlines()


def extract_info(step: int) -> tuple[bool, int, int]:
    relevant_instructions = puzzle_input[step * 18 : (step + 1) * 18]
    divz26 = int(relevant_instructions[4].split()[2]) == 26
    var1 = int(relevant_instructions[5].split()[2])
    var2 = int(relevant_instructions[15].split()[2])
    return (divz26, var1, var2)


def get_z(model_num: str, steps: int = 14) -> int:
    z = 0
    for input, step in zip(model_num, range(steps)):
        w = int(input)
        divz26, var1, var2 = extract_info(step)
        z = run_round(z, w, divz26, var1, var2)
    return z


def run_round(z: int, w: int, divz26: bool, var1: int, var2: int) -> int:
    x = z % 26 + var1
    if divz26:
        z //= 26
        if x != w:
            return -1
    if x != w:
        z = 26 * z + w + var2
    return z


valid_z: dict[int, str] = {0: ""}  # from z value to high input
for step in range(14):
    divz26, var1, var2 = extract_info(step)
    new_valid_z: dict[int, str] = {}
    for z, input in valid_z.items():
        for n in range(9, 0, -1):
            new_z = run_round(z, n, divz26, var1, var2)
            if new_z == -1:
                continue
            new_valid_z[new_z] = input + str(n)
    valid_z = new_valid_z
pprint(valid_z)
