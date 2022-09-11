puzzle_input = "171309-643603"

lower_bound, upper_bound = [int(x) for x in puzzle_input.split("-")]


def is_valid_password(password):
    password_str = str(password)
    same_adjacent_digits = False
    for i in range(len(password_str) - 1):
        sub_str = password_str[i : i + 2]
        if sub_str[0] == sub_str[1]:
            same_adjacent_digits = True
        if int(sub_str[0]) > int(sub_str[1]):
            return False
    return same_adjacent_digits


n = 0
for cur_password in range(lower_bound, upper_bound + 1):
    if is_valid_password(cur_password):
        n += 1

print(n)
