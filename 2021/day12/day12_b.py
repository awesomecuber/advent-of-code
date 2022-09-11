import pprint
import os
import sys

with open(os.path.join(sys.path[0], "day12.txt")) as f:
    puzzle_input = f.read().splitlines()

edges: list[tuple[str, str]] = [
    (x.split("-")[0], x.split("-")[1]) for x in puzzle_input
]
connected_to: dict[str, set[str]] = {}
for vertex1, vertex2 in edges:
    if vertex1 not in connected_to:
        connected_to[vertex1] = set()
    if vertex2 not in connected_to:
        connected_to[vertex2] = set()
    connected_to[vertex1].add(vertex2)
    connected_to[vertex2].add(vertex1)


def num_paths(start_vertex: str, no_revisit: set[str], has_double_visited: bool) -> int:
    if start_vertex == "end":
        return 1
    to_return = 0
    no_revisit_copy = no_revisit.copy()
    if start_vertex.islower():
        no_revisit_copy.add(start_vertex)
    for connected in connected_to[start_vertex]:
        if connected in no_revisit and not has_double_visited and connected != "start":
            to_return += num_paths(connected, no_revisit_copy, True)
        elif connected not in no_revisit:
            to_return += num_paths(connected, no_revisit_copy, has_double_visited)
    return to_return


print(num_paths("start", set(), False))
