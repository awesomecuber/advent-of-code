import collections
import time

# puzzle_input = '389125467' # example
puzzle_input = '418976235' # actual

cups = collections.deque([int(x) for x in puzzle_input])
for x in range(10, 1000001):
    cups.append(x)
MAX_CUP = 1000000
# MAX_CUP = 9

start_time = time.perf_counter()

to_insert: dict[int, list[int]] = {}
for _ in range(10000000):
    current_cup = cups.popleft()
    if current_cup in to_insert:
        cups.appendleft(to_insert[current_cup][2])
        cups.appendleft(to_insert[current_cup][1])
        cups.appendleft(to_insert[current_cup][0])
        del to_insert[current_cup]
    cups.append(current_cup)
    cups_removed = []
    for _ in range(3):
        next_cup = cups.popleft()
        cups_removed.append(next_cup)
        if next_cup in to_insert:
            cups.appendleft(to_insert[next_cup][2])
            cups.appendleft(to_insert[next_cup][1])
            cups.appendleft(to_insert[next_cup][0])
            del to_insert[next_cup]

    destination_cup = current_cup - 1 if current_cup > 1 else MAX_CUP
    while destination_cup in cups_removed:
        destination_cup = destination_cup - 1 if destination_cup > 1 else MAX_CUP
    to_insert[destination_cup] = cups_removed

print(time.perf_counter() - start_time)

while len(to_insert) > 0:
    next_cup = cups.popleft()
    if next_cup in to_insert:
        cups.appendleft(to_insert[next_cup][2])
        cups.appendleft(to_insert[next_cup][1])
        cups.appendleft(to_insert[next_cup][0])
        del to_insert[next_cup]
    cups.append(next_cup)

start = cups.popleft()
while start != 1:
    cups.append(start)
    start = cups.popleft()

print(cups.popleft() * cups.popleft())