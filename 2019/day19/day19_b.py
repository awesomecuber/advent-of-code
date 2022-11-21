from intcode import IntCodeProgram

drone_system = IntCodeProgram("day19.txt")

top_band: set[tuple[int, int]] = set()
bottom_band: set[tuple[int, int]] = set()

x = 0
y = 0
while True:
    (drone_status,) = drone_system.run([x, y])
    if drone_status == 1:
        top_band.add((x, y))
print(total)
