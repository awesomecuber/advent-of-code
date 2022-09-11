import math
import os
import sys

with open(os.path.join(sys.path[0], "day13.txt")) as f:
    puzzle_input = f.read().splitlines()

buses = [(i, int(x)) for i, x in enumerate(puzzle_input[1].split(",")) if x != "x"]

t = 0
increment = 1
place = 0
while not all([(t + i) % x == 0 for i, x in buses]):
    if (t + buses[place][0]) % buses[place][1] == 0:
        increment = int(
            (increment * buses[place][1]) / math.gcd(increment, buses[place][1])
        )
        place += 1
        print("new increment", increment)
    t += increment
print(t)
