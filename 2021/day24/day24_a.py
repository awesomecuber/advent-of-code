# from itertools import product
import os
import random
import sys

with open(os.path.join(sys.path[0], "day24.txt")) as f:
    puzzle_input = f.read().splitlines()

variables = {
    'w': 0,
    'x': 0,
    'y': 0,
    'z': 0
}

def val(b: str):
    try:
        return int(b)
    except Exception:
        return variables[b]

def reset_variables():
    variables['w'] = 0
    variables['x'] = 0
    variables['y'] = 0
    variables['z'] = 0

def get_z(model_num: str, steps: int = 14) -> int:
    reset_variables()
    inp_count = 0
    for instruction in puzzle_input[:steps * 18]:
        match instruction.split():
            case ('inp', a):
                variables[a] = int(model_num[inp_count])
                inp_count += 1
            case ('add', a, b):
                variables[a] += val(b)
            case ('mul', a, b):
                variables[a] *= val(b)
            case ('div', a, b):
                variables[a] //= val(b)
            case ('mod', a, b):
                variables[a] %= val(b)
            case ('eql', a, b):
                variables[a] = int(variables[a] == val(b))
    return variables['z']

def get_max_model_num(z: int = 0, step: int = 0) -> int:
    z_div_26 = True if int(puzzle_input[step * 18 + 4].split()[2]) == 26 else False
    equality_add = int(puzzle_input[step * 18 + 5].split()[2])
    z_add = int(puzzle_input[step * 18 + 15].split()[2])

    for n in range(9, 0, -1):
        new_z = z
        if z_div_26:
            if (z % 26) + equality_add == n:
                new_z //= 26
                if step > 8:
                    print(step, new_z)
            else:
                # MY GUESS IS THAT IF IT GOES HERE, Z WON'T BE ZERO
                break
        else:
            new_z = 26 * new_z + n + z_add
        hm = get_max_model_num(new_z, step + 1)
        if hm != -1:
            return hm
    return -1

def reverse_engineer(model_num: str, steps: int = 14) -> int:
    ns = list(map(int, list(model_num)))
    z_div_26s: list[bool] = []
    equality_adds: list[int] = []
    z_adds: list[int] = []
    for step in range(steps):
        z_div_26s.append(True if int(puzzle_input[step * 18 + 4].split()[2]) == 26 else False)
        equality_adds.append(int(puzzle_input[step * 18 + 5].split()[2]))
        z_adds.append(int(puzzle_input[step * 18 + 15].split()[2]))

    z = 0
    z_mods: list[int] = []
    for step in range(steps):
        if z_div_26s[step]:
            if (z % 26) + equality_adds[step] == ns[step]:
                print('we in')
                z //= 26
            else:
                # MY GUESS IS THAT IF IT GOES HERE, Z WON'T BE ZERO
                z = z - (z % 26) + ns[step] + z_adds[step]
        else:
            z = 26 * z + ns[step] + z_adds[step]
        z_mods.append(z % 26)
    
    for a in zip(ns, z_div_26s, equality_adds, z_adds, z_mods):
        if a[1]:
            print(a)
        guess = 0
        if a[1] and (a[4] + a[2] == a[0]):
            guess = 0
        else:
            guess = a[0] + a[3]
        print(a[4], guess)
    # print(ns)
    # print(z_div_26s)
    # print(equality_adds)
    # print(z_adds)
    # print(z_mods)
    return z

# for _ in range(1000):
#     model_num = ''
#     for _ in range(14):
#         model_num += str(random.randint(1, 9))
#     if reverse_engineer(model_num) != get_z(model_num):
#         print('error!', model_num)

# print(get_z('13579246899999'))
# print(reverse_engineer('99999999999999'))
print(get_max_model_num())

# print((get_z('1111', 4) // 26) % 26 - 8)
# print(get_z('11111', 5))

# for n1, n2 in product(range(1, 10), repeat=2):
#     print(n1, n2, get_z(''.join([str(n1), str(n2)])))

# 5 5 5

# z = 12
# z = 26(12) + 5 + 8 = 325
# z = 26(325) + 5 + 16 = 8471
# z = 26(8471) + 5 + 8 = 220249