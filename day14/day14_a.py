with open("day14.txt") as f:
    puzzle_input = f.read().splitlines()

mask = ""
memory = {}
for line in puzzle_input:
    if line[:4] == "mask":
        mask = line[7:]
    else:
        memory_address = int(line[4:line.find("]")])
        num_binary = bin(int(line.split(" = ")[1]))[2:].zfill(36)
        
        for index, letter in enumerate(mask):
            if letter in ["0", "1"]:
                num_binary = num_binary[:index] + letter + num_binary[index + 1:]
        memory[memory_address] = int(num_binary, 2)

total_size = 0
for address in memory:
    total_size += memory[address]

print(total_size)