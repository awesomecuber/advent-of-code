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
pois: dict[str, coord] = {}
for y, line in enumerate(vault):
    for x, char in enumerate(line):
        if char == "@" or char.isalpha():
            pois[char] = (x, y)


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
    horizon = [pois["@"]]
    seen: dict[coord, set[str]] = {
        pois["@"]: set()
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


def get_possible_next_keys(
    key_reqs: dict[str, set[str]], own_keys: frozenset[str]
) -> set[str]:
    to_return = set()
    for key, reqs in key_reqs.items():
        if key not in own_keys and reqs <= own_keys:
            to_return.add(key)
    return to_return


def get_dist(vault: list[str], start: coord, end: coord) -> int:
    """Returns -1 if you can't reach end without passing through walls"""
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
    pos: str
    keys_so_far: frozenset[str]


key_reqs = get_key_reqs(vault)
num_keys = len([k for k in pois.keys() if k.islower()])

dist_cache: dict[tuple[str, str], int] = {}

init = MazeState("@", frozenset())

horizon: list[tuple[int, MazeState]] = []
heappush(horizon, (0, init))
dists = {init: 0}
while len(horizon) > 0:
    dist, cur = heappop(horizon)
    if len(cur.keys_so_far) == num_keys:
        print(dist)
        break
    for next_key in get_possible_next_keys(key_reqs, cur.keys_so_far):
        next = MazeState(next_key, cur.keys_so_far | set(next_key))
        if (cur.pos, next_key) in dist_cache:
            dist_incr = dist_cache[cur.pos, next_key]
        else:
            dist_incr = get_dist(vault, pois[cur.pos], pois[next_key])
            dist_cache[cur.pos, next_key] = dist_incr
            dist_cache[next_key, cur.pos] = dist_incr
        if dist_incr == -1:
            continue
        if next not in dists or dist + dist_incr < dists[next]:
            heappush(horizon, (dist + dist_incr, next))
            dists[next] = dist + dist_incr
