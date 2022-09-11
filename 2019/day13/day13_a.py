from intcode import IntCodeProgram

arcade = IntCodeProgram("day13.txt")
output = arcade.run()

tiles = []
while len(output) > 0:
    tiles.append(tuple(output[:3]))
    output = output[3:]

print(len(list(tile for tile in tiles if tile[2] == 2)))
