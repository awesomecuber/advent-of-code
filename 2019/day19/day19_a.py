from intcode import IntCodeProgram

drone_system = IntCodeProgram("day19.txt")

total = 0
for y in range(50):
    for x in range(50):
        (drone_status,) = drone_system.run([x, y])
        total += drone_status
print(total)
