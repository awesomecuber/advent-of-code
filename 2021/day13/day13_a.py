import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day13.txt")) as f:
    puzzle_input = f.read().splitlines()

point_locations = puzzle_input[: puzzle_input.index("")]
fold_instructions = puzzle_input[puzzle_input.index("") + 1 :]
points: set[tuple[int, int]] = set(
    (int(x.split(",")[0]), int(x.split(",")[1])) for x in point_locations
)

for fold_instruction in fold_instructions:
    axis = fold_instruction[11]
    fold_location = int(fold_instruction[13:])

    old_points = points.copy()
    for point in old_points:
        if axis == "x" and point[0] > fold_location:
            points.remove(point)
            points.add((2 * fold_location - point[0], point[1]))
        if axis == "y" and point[1] > fold_location:
            points.remove(point)
            points.add((point[0], 2 * fold_location - point[1]))

for y_level in range(max(point[1] for point in points) + 1):
    for x_level in range(max(point[0] for point in points) + 1):
        if (x_level, y_level) in points:
            print("#", end="")
        else:
            print(".", end="")
    print()
