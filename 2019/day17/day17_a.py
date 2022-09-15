from intcode import IntCodeProgram

camera = IntCodeProgram("day17.txt")
outputs = camera.run()
picture = "".join(map(chr, outputs)).splitlines()[:-1]

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


answer = 0
for y in range(len(picture)):
    for x in range(len(picture[0])):
        if is_intersection(picture, x, y):
            answer += x * y

print(answer)
