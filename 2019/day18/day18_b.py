from heapq import heappop, heappush
import os
import sys
from typing import NamedTuple

with open(os.path.join(sys.path[0], "day18.txt")) as f:
    vault = f.read().splitlines()

coord = tuple[int, int]

# points of interest:
# - @: start
# - lowercase: key
# - uppercase: door
multiple_at = False
pois: dict[str, coord] = {}
for y, line in enumerate(vault):
    for x, char in enumerate(line):
        if char == "@" or char.isalpha():
            if char == "@" and "@" in pois:
                multiple_at = True
            pois[char] = (x, y)

x, y = pois["@"]
del pois["@"]
if multiple_at:
    # get the middle square
    x = x - 1
    y = y - 1
else:
    # update vault
    vault[y - 1] = vault[y - 1][: x - 1] + "@#@" + vault[y - 1][x + 2 :]
    vault[y] = vault[y][: x - 1] + "###" + vault[y][x + 2 :]
    vault[y + 1] = vault[y + 1][: x - 1] + "@#@" + vault[y + 1][x + 2 :]
pois["@1"] = (x - 1, y - 1)
pois["@2"] = (x + 1, y - 1)
pois["@3"] = (x - 1, y + 1)
pois["@4"] = (x + 1, y + 1)


def get_neighbors(vault: list[str], pos: coord) -> list[coord]:
    x, y = pos
    to_return = []
    if vault[y][x - 1] != "#":
        to_return.append((x - 1, y))
    if vault[y][x + 1] != "#":
        to_return.append((x + 1, y))
    if vault[y - 1][x] != "#":
        to_return.append((x, y - 1))
    if vault[y + 1][x] != "#":
        to_return.append((x, y + 1))
    return to_return


def print_vault(vault: list[str], seen: set[coord]):
    for y, line in enumerate(vault):
        for x, char in enumerate(line):
            if (x, y) in seen:
                print("O", end="")
            else:
                print(char, end="")
        print()


# this code reveals that v = 63 and 2e = 124
# since in a connected tree, v = e-1, this proves
# that our maze is a tree, and therefore that
# there are no loops
#
# v = 0
# two_e = 0
# for y, line in enumerate(vault):
#     for x, char in enumerate(line):
#         if char != "#":
#             v += 1
#             two_e += len(get_neighbors(vault, (x, y)))
# print(v, two_e)


def get_key_reqs(vault: list[str]) -> dict[str, set[str]]:
    key_reqs: dict[str, set[str]] = {}
    horizon = [pois["@1"], pois["@2"], pois["@3"], pois["@4"]]
    seen: dict[coord, set[str]] = {
        pois["@1"]: set(),
        pois["@2"]: set(),
        pois["@3"]: set(),
        pois["@4"]: set(),
    }  # also keeps track of the doors it takes to get to the place
    while len(horizon) > 0:
        next = horizon.pop()
        char = vault[next[1]][next[0]]
        if char.islower():
            key_reqs[char] = seen[next]
        for neighbor in get_neighbors(vault, next):
            if neighbor not in seen:
                horizon.append(neighbor)
                seen[neighbor] = seen[next].copy()
                neighbor_char = vault[neighbor[1]][neighbor[0]]
                if neighbor_char.isupper():
                    seen[neighbor].add(neighbor_char.lower())
    return key_reqs


def get_reachable_keys(vault: list[str], start: coord) -> set[str]:
    keys: set[str] = set()
    horizon = [start]
    seen = {start}
    while len(horizon) > 0:
        next = horizon.pop()
        char = vault[next[1]][next[0]]
        if char.islower():
            keys.add(char)
        for neighbor in get_neighbors(vault, next):
            if neighbor not in seen:
                horizon.append(neighbor)
                seen.add(neighbor)
    return keys


def get_possible_next_keys(
    key_reqs: dict[str, set[str]], own_keys: frozenset[str]
) -> set[str]:
    to_return = set()
    for key, reqs in key_reqs.items():
        if key not in own_keys and reqs <= own_keys:
            to_return.add(key)
    return to_return


def get_dist(vault: list[str], start: coord, end: coord) -> int:
    """Returns -1 if you can't reach end without passing through walls or keys"""
    horizon: list[tuple[int, coord]] = []
    heappush(horizon, (0, start))
    seen: set[coord] = {start}
    while len(horizon) > 0:
        dist, next = heappop(horizon)
        if next == end:
            return dist
        for neighbor in get_neighbors(vault, next):
            if neighbor not in seen:
                heappush(horizon, (dist + 1, neighbor))
                seen.add(neighbor)
    return -1


class MazeState(NamedTuple):
    pos1: str
    pos2: str
    pos3: str
    pos4: str
    keys_so_far: frozenset[str]


key_reqs = get_key_reqs(vault)
num_keys = len([k for k in pois.keys() if k.islower()])

keys1 = get_reachable_keys(vault, pois["@1"])
keys2 = get_reachable_keys(vault, pois["@2"])
keys3 = get_reachable_keys(vault, pois["@3"])
keys4 = get_reachable_keys(vault, pois["@4"])

dist_cache: dict[tuple[str, str], int] = {}

init = MazeState("@1", "@2", "@3", "@4", frozenset())

horizon: list[tuple[int, MazeState]] = []
heappush(horizon, (0, init))
dists = {init: 0}
while len(horizon) > 0:
    dist, cur = heappop(horizon)
    # print(f"{len(cur.keys_so_far)}/{num_keys}")
    if len(cur.keys_so_far) == num_keys:
        print(dist)
        break
    for next_key in get_possible_next_keys(key_reqs, cur.keys_so_far):
        new_keys_seen = cur.keys_so_far | set(next_key)
        if next_key in keys1:
            move_pos = cur.pos1
            next = MazeState(next_key, cur.pos2, cur.pos3, cur.pos4, new_keys_seen)
        elif next_key in keys2:
            move_pos = cur.pos2
            next = MazeState(cur.pos1, next_key, cur.pos3, cur.pos4, new_keys_seen)
        elif next_key in keys3:
            move_pos = cur.pos3
            next = MazeState(cur.pos1, cur.pos2, next_key, cur.pos4, new_keys_seen)
        elif next_key in keys4:
            move_pos = cur.pos4
            next = MazeState(cur.pos1, cur.pos2, cur.pos3, next_key, new_keys_seen)

        if (move_pos, next_key) in dist_cache:
            dist_incr = dist_cache[move_pos, next_key]
        else:
            dist_incr = get_dist(vault, pois[move_pos], pois[next_key])
            dist_cache[move_pos, next_key] = dist_incr
            dist_cache[next_key, move_pos] = dist_incr
        if dist_incr == -1:
            continue
        if next not in dists or dist + dist_incr < dists[next]:
            heappush(horizon, (dist + dist_incr, next))
            dists[next] = dist + dist_incr
