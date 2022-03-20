from copy import deepcopy
from enum import Enum
from functools import cache
from itertools import chain, takewhile
import os
import sys

with open(os.path.join(sys.path[0], "day23.txt")) as f:
    puzzle_input = f.read().splitlines()

class Amphipod(Enum):
    A = 1
    B = 10
    C = 100
    D = 1000

# rooms = {
#     2: [Amphipod[puzzle_input[3][3]], Amphipod[puzzle_input[2][3]]],
#     4: [Amphipod[puzzle_input[3][5]], Amphipod[puzzle_input[2][5]]],
#     6: [Amphipod[puzzle_input[3][7]], Amphipod[puzzle_input[2][7]]],
#     8: [Amphipod[puzzle_input[3][9]], Amphipod[puzzle_input[2][9]]]
# }

rooms = {
    2: [Amphipod[puzzle_input[3][3]], Amphipod.D, Amphipod.D, Amphipod[puzzle_input[2][3]]],
    4: [Amphipod[puzzle_input[3][5]], Amphipod.B, Amphipod.C, Amphipod[puzzle_input[2][5]]],
    6: [Amphipod[puzzle_input[3][7]], Amphipod.A, Amphipod.B, Amphipod[puzzle_input[2][7]]],
    8: [Amphipod[puzzle_input[3][9]], Amphipod.C, Amphipod.A, Amphipod[puzzle_input[2][9]]]
}

ROOM_SIZE = len(rooms[2])

hallway: list[Amphipod | None] = [None] * 11

def possible_to_leave(pos: int, room: list[Amphipod]):
    if len(room) == 0:
        return False
    if pos == 2 and all(pos == Amphipod.A for pos in room):
        return False
    if pos == 4 and all(pos == Amphipod.B for pos in room):
        return False
    if pos == 6 and all(pos == Amphipod.C for pos in room):
        return False
    if pos == 8 and all(pos == Amphipod.D for pos in room):
        return False
    return True

def get_destination_room(amphipod: Amphipod):
    if amphipod == Amphipod.A:
        return 2
    if amphipod == Amphipod.B:
        return 4
    if amphipod == Amphipod.C:
        return 6
    if amphipod == Amphipod.D:
        return 8

def freeze_rooms(rooms: dict[int, list[Amphipod]]) -> tuple[tuple[Amphipod,...],...]:
    return tuple(map(tuple, rooms.values())) # type: ignore

@cache
def best_energy(
        room_values: tuple[tuple[Amphipod,...],...],
        hallway: tuple[Amphipod | None]
    ) -> int:

    rooms = {
        2: list(room_values[0]),
        4: list(room_values[1]),
        6: list(room_values[2]),
        8: list(room_values[3]),
    }
    if all(not possible_to_leave(pos, room) and len(room) == ROOM_SIZE for pos, room in rooms.items()):
        return 0
    all_energies: list[int] = [sys.maxsize]

    for pos, moving in enumerate(hallway):
        if moving is None:
            continue

        destination_room = get_destination_room(moving)
        possible_destinations = list(chain(
            takewhile(lambda x: hallway[x] is None, range(pos + 1, 11)),
            takewhile(lambda x: hallway[x] is None, range(pos - 1, -1, -1))
        ))

        if (not possible_to_leave(destination_room, rooms[destination_room])
                and destination_room in possible_destinations):
            new_rooms = deepcopy(rooms)
            new_rooms[destination_room].append(moving)
            new_hallway = list(deepcopy(hallway))
            new_hallway[pos] = None
            move_energy = abs(destination_room - pos) * moving.value
            enter_energy = moving.value * (ROOM_SIZE + 1 - len(new_rooms[destination_room]))
            total_energy = move_energy + enter_energy
            all_energies.append(
                total_energy + best_energy(freeze_rooms(new_rooms), tuple(new_hallway))
            )

    can_leave = {pos: room for pos, room in rooms.items() if possible_to_leave(pos, room)}
    for pos, room in can_leave.items():
        moving = room[-1]
        destination_room = get_destination_room(moving)
        leave_energy = moving.value * (ROOM_SIZE + 1 - len(room))

        possible_destinations = list(chain(
            takewhile(lambda x: hallway[x] is None, range(pos + 1, 11)),
            takewhile(lambda x: hallway[x] is None, range(pos - 1, -1, -1))
        ))

        if (not possible_to_leave(destination_room, rooms[destination_room])
                and destination_room in possible_destinations):
            new_rooms = deepcopy(rooms)
            moving = new_rooms[pos].pop()
            new_rooms[destination_room].append(moving)
            move_energy = abs(destination_room - pos) * moving.value
            enter_energy = moving.value * (ROOM_SIZE + 1 - len(new_rooms[destination_room]))
            total_energy = leave_energy + move_energy + enter_energy
            all_energies.append(
                total_energy + best_energy(freeze_rooms(new_rooms), hallway)
            )
        else:
            for i in possible_destinations:
                if i not in rooms.keys():
                    new_rooms = deepcopy(rooms)
                    moving = new_rooms[pos].pop()
                    new_hallway = list(deepcopy(hallway))
                    new_hallway[i] = moving
                    move_energy = abs(i - pos) * moving.value
                    total_energy = leave_energy + move_energy
                    all_energies.append(
                        total_energy + best_energy(freeze_rooms(new_rooms), tuple(new_hallway))
                    )

    return min(all_energies)

print(best_energy(freeze_rooms(rooms), tuple(hallway)))