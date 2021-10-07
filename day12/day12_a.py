with open("day12.txt") as f:
    puzzle_input = f.read().splitlines()

position = [0, 0]
direction = 1 # N E S W
for line in puzzle_input:
    command = line[:1]
    amount = int(line[1:])
    if command == "F":
        if direction == 0:
            command = "N"
        elif direction == 1:
            command = "E"
        elif direction == 2:
            command = "S"
        elif direction == 3:
            command = "W"

    if command == "N":
        position[0] += amount
    elif command == "S":
        position[0] -= amount
    elif command == "E":
        position[1] += amount
    elif command == "W":
        position[1] -= amount
    elif command == "L":
        direction = (direction - int(amount / 90)) % 4
    elif command == "R":
        direction = (direction + int(amount / 90)) % 4

print(abs(position[0]) + abs(position[1]))