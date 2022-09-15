from pprint import pprint

from intcode import ExitCode, IntCodeProgram

camera = IntCodeProgram("day17.txt")
outputs = camera.run()
picture = "".join(map(chr, outputs)).splitlines()[:-1]
camera.reset()

WIDTH = len(picture[0])
HEIGHT = len(picture)


def is_intersection(picture: list[str], x: int, y: int) -> bool:
    if x == 0 or x == WIDTH - 1 or y == 0 or y == HEIGHT - 1:
        return False
    return (
        picture[y][x] == "#"
        and picture[y][x - 1] == "#"
        and picture[y][x + 1] == "#"
        and picture[y - 1][x] == "#"
        and picture[y + 1][x] == "#"
    )


def turn_right(cur_dir: tuple[int, int]) -> tuple[int, int]:
    return -cur_dir[1], cur_dir[0]


def turn_left(cur_dir: tuple[int, int]) -> tuple[int, int]:
    return cur_dir[1], -cur_dir[0]


def in_front(pos: tuple[int, int], cur_dir: tuple[int, int]) -> tuple[int, int]:
    return pos[0] + cur_dir[0], pos[1] + cur_dir[1]


def char_at(picture: list[str], pos: tuple[int, int]) -> str:
    if pos[0] < 0 or pos[0] >= WIDTH or pos[1] < 0 or pos[1] >= HEIGHT:
        return "."
    return picture[pos[1]][pos[0]]


position = (0, 0)
direction = (0, 0)
# find arrow and direction
for (y, line) in enumerate(picture):
    for (x, char) in enumerate(line):
        if char not in (".", "#"):
            position = (x, y)
            if char == "^":
                direction = (0, -1)
            elif char == "v":
                direction = (0, 1)
            elif char == "<":
                direction = (-1, 0)
            elif char == ">":
                direction = (1, 0)

instructions: list[str] = []
streak = 0

while True:
    if char_at(picture, in_front(position, direction)) == "#":
        position = in_front(position, direction)
        streak += 1
    else:
        if streak != 0:
            instructions.append(str(streak))
            streak = 0

        left_dir = turn_left(direction)
        right_dir = turn_right(direction)
        if char_at(picture, in_front(position, left_dir)) == "#":
            direction = left_dir
            instructions.append("L")
        elif char_at(picture, in_front(position, right_dir)) == "#":
            direction = right_dir
            instructions.append("R")
        else:
            break
print(",".join(instructions))

# at this point, i manually inspected the instructions and broke it up into the following
#
# read from left to right, top to bottom
# R,10,L,8,R,10,R,4  L,6,L,6,R,10  R,10,L,8,R,10,R,4, L,6,R,12,R,12,R,10
#                    L,6,L,6,R,10                     L,6,R,12,R,12,R,10
# R,10,L,8,R,10,R,4  L,6,L,6,R,10  R,10,L,8,R,10,R,4  L,6,R,12,R,12,R,10

camera.set_mem(0, 2)

a = "R,10,L,8,R,10,R,4"
b = "L,6,L,6,R,10"
c = "L,6,R,12,R,12,R,10"
main = "A,B,A,C,B,C,A,B,A,C"

inputs = list(map(ord, "\n".join([main, a, b, c, "n"]) + "\n"))
outputs = camera.run(inputs)
print(outputs[-1])

# use this if you're viewing output
#
# for input in inputs:
#     camera.add_input(input)
# while True:
#     outputs, err = camera.get_n_outputs(WIDTH * (HEIGHT + 1) - 3)
#     if err != ExitCode.HALTED:
#         print(err)
#         break
#     print("".join(map(chr, outputs)), end="")
