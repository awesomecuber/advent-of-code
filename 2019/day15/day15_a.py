from enum import Enum
import time

from intcode import IntCodeProgram

class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

DIR_OFFSET = {
    Direction.NORTH: (0, -1),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
    Direction.EAST: (1, 0)
}

DIR_OPPOSITE = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST,
    Direction.EAST: Direction.WEST
}

MANUAL = False

arcade = IntCodeProgram('day15.txt')
bot_location = (0, 0)

area: dict[tuple[int, int], str] = {}
area[0, 0] = 'D'

def add_coords(a: tuple[int, int], b: tuple[int, int]):
    return (a[0] + b[0], a[1] + b[1])

def print_area(area):
    min_x = min(x for x, _ in area)
    max_x = max(x for x, _ in area)
    min_y = min(y for _, y in area)
    max_y = max(y for _, y in area)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in area:
                print(area[x, y], end='')
            else:
                print(' ', end='')
        print()

def get_new_direction(area, coord):
    for direction, offset in DIR_OFFSET.items():
        if add_coords(coord, offset) not in area:
            return direction
    return None

so_far: list[Direction] = []
while True:
    # print_area(area)
    back_track = False

    if MANUAL:
        dir_input = input('What direction? (n/s/w/e): ')
        match dir_input:
            case 'n':
                direction = Direction.NORTH
            case 's':
                direction = Direction.SOUTH
            case 'w':
                direction = Direction.WEST
            case 'e':
                direction = Direction.EAST
    else:
        direction = get_new_direction(area, bot_location)
        if direction == None:
            back_track = True
            direction = DIR_OPPOSITE[so_far.pop()]

    new_location = add_coords(bot_location, DIR_OFFSET[direction])
    arcade.add_input(direction.value)
    output, _ = arcade.get_one_output()
    match output:
        case 0:
            area[new_location] = '#'
        case 1:
            area[bot_location] = '.'
            bot_location = new_location
            area[bot_location] = 'D'
            if not back_track:
                so_far.append(direction)
        case 2:
            area[bot_location] = '.'
            bot_location = new_location
            area[bot_location] = 'D'
            so_far.append(direction)
            print_area(area)
            print('HOLY SHIT YOU FOUND IT')
            print(len(so_far))
            break