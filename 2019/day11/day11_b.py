from intcode import IntCodeProgram

brain = IntCodeProgram('day11.txt')

# normal cartesian grid
cur_spot = (0, 0)
heading = (0, 1)
white_panels = set()

white_panels.add((0, 0))

def rotate_cw(heading):
    return heading[1], -heading[0]

def rotate_ccw(heading):
    return -heading[1], heading[0]

def new_spot(cur_spot, heading):
    return cur_spot[0] + heading[0], cur_spot[1] + heading[1]

while True:
    brain.add_input(1 if cur_spot in white_panels else 0)
    new_color_output = brain.get_one_output()
    if new_color_output is None:
        break
    new_heading_output = brain.get_one_output()
    if new_heading_output is None:
        break

    if new_color_output == 0:
        white_panels.discard(cur_spot)
    else: # its 1
        white_panels.add(cur_spot)

    if new_heading_output == 0:
        heading = rotate_ccw(heading)
    else: # its 1
        heading = rotate_cw(heading)

    cur_spot = new_spot(cur_spot, heading)

min_x = min(x for x, _ in white_panels)
max_x = max(x for x, _ in white_panels)
min_y = min(y for _, y in white_panels)
max_y = max(y for _, y in white_panels)

for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
        if (x, y) in white_panels:
            print('#', end='')
        else:
            print('.', end='')
    print()
# (it's upside down lol)