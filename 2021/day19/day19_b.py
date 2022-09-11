import copy
from itertools import combinations, permutations, product
import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day19.txt")) as f:
    puzzle_input = f.read().splitlines()

relative_scanners: list[set[tuple[int, int, int]]] = []

while len(puzzle_input) > 0:
    if "" in puzzle_input:
        space = puzzle_input.index("")
    else:
        space = -1
    scanner = set(tuple(map(int, x.split(","))) for x in puzzle_input[1:space])
    relative_scanners.append(scanner)  # type: ignore
    puzzle_input = puzzle_input[space + 1 :]
    if space == -1:
        puzzle_input = []


def orientations(scanner):
    def x(scanner: set[tuple[int, int, int]]):
        return set((point[0], point[2], -point[1]) for point in scanner)

    def y(scanner):
        return set((-point[2], point[1], point[0]) for point in scanner)

    scanner_copy = copy.deepcopy(scanner)
    for _ in range(3):
        for _ in range(4):
            yield scanner_copy
            scanner_copy = y(scanner_copy)
        scanner_copy = x(scanner_copy)
    for _ in range(2):
        for _ in range(3):
            yield scanner_copy
            scanner_copy = y(scanner_copy)
        yield scanner_copy
        scanner_copy = x(scanner_copy)
    scanner_copy = x(scanner_copy)
    yield scanner_copy
    for _ in range(3):
        scanner_copy = y(scanner_copy)
        yield scanner_copy


def all_deltas(scanner1, scanner2):
    for point1, point2 in product(scanner1, scanner2):
        yield (point1[0] - point2[0], point1[1] - point2[1], point1[2] - point2[2])


def tuple_add(tuple1, tuple2):
    return tuple(a + b for a, b in zip(tuple1, tuple2))


scanner_locations: set[tuple[int, int, int]] = set()


def is_match(objective_scanner, relative_scanner):
    global scanner_locations
    for other_scanner in orientations(relative_scanner):
        for delta in all_deltas(objective_scanner, other_scanner):
            matches = 0
            for other_point in other_scanner:
                if tuple_add(other_point, delta) in objective_scanner:
                    matches += 1
            if matches >= 6:  # wont work with more???
                print(delta)
                scanner_locations.add(delta)
                return set(
                    tuple_add(other_point, delta) for other_point in other_scanner
                )
    return set()


# for i, j in combinations(range(26), 2):
#     if j == 25 and len(is_match(relative_scanners[i], relative_scanners[j])):
#         print(i, j)


objective_scanners: list[set[tuple[int, int, int]]] = []
objective_scanners.append(relative_scanners.pop(0))

cur_objective_scanners = objective_scanners.copy()

while len(cur_objective_scanners) > 0:
    print(len(cur_objective_scanners), len(relative_scanners))
    to_remove: set[int] = set()
    new_objective_scanners: list[set[tuple[int, int, int]]] = []
    for objective_scanner, (i, relative_scanner) in product(
        cur_objective_scanners, enumerate(relative_scanners)
    ):
        if i in to_remove:
            continue
        possible_new_objective_scanner = is_match(objective_scanner, relative_scanner)
        if len(possible_new_objective_scanner) > 0:
            to_remove.add(i)
            new_objective_scanners.append(possible_new_objective_scanner)
    for i in sorted(to_remove, reverse=True):
        del relative_scanners[i]
    objective_scanners += new_objective_scanners
    cur_objective_scanners = new_objective_scanners

print(relative_scanners)

all_beacons = set()
for a_scanner in objective_scanners:
    for beacon in a_scanner:
        all_beacons.add(beacon)

max_dist = 0
for scanner1, scanner2 in combinations(scanner_locations, 2):
    man_dist = (
        abs(scanner1[0] - scanner2[0])
        + abs(scanner1[1] - scanner2[1])
        + abs(scanner1[2] - scanner2[2])
    )
    max_dist = max(max_dist, man_dist)

print(max_dist)
