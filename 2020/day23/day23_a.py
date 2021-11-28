import collections

puzzle_input = '389125467' # example
# puzzle_input = '418976235' # actual

cups = collections.deque([int(x) for x in puzzle_input])

for _ in range(100):
    current_cup = cups.popleft()
    cups.append(current_cup)
    cup1 = cups.popleft()
    cup2 = cups.popleft()
    cup3 = cups.popleft()

    destination_cup = current_cup - 1 if current_cup > 1 else 9
    while destination_cup not in cups:
        destination_cup = destination_cup - 1 if destination_cup > 1 else 9
    
    destination_position = cups.index(destination_cup)
    cups.insert(destination_position + 1, cup3)
    cups.insert(destination_position + 1, cup2)
    cups.insert(destination_position + 1, cup1)
    print(int(''.join([str(x) for x in cups])))

start = cups.popleft()
while start != 1:
    cups.append(start)
    start = cups.popleft()

print(int(''.join([str(x) for x in cups])))