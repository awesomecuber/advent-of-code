with open("day14.txt") as f:
    puzzle_input = f.read().splitlines()

def write_memory(num_binary, value):
    x_index = num_binary.find("X")
    if x_index == -1:
        memory[int(num_binary, 2)] = value
    else:
        write_memory(num_binary[:x_index] + "0" + num_binary[x_index + 1:], value)
        write_memory(num_binary[:x_index] + "1" + num_binary[x_index + 1:], value)

mask = ""
memory = {}
for line in puzzle_input:
    if line[:4] == "mask":
        mask = line[7:]
    else:
        memory_address = int(line[4:line.find("]")])
        num_binary = bin(memory_address)[2:].zfill(36)
        value = int(line.split(" = ")[1])
        
        for index, letter in enumerate(mask):
            if letter in ["1", "X"]:
                num_binary = num_binary[:index] + letter + num_binary[index + 1:]
        write_memory(num_binary, value)

total_size = 0
for address in memory:
    total_size += memory[address]

print(total_size)