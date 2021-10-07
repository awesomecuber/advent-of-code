puzzle_input = "171309-643603"

lower_bound, upper_bound = [int(x) for x in puzzle_input.split("-")]

def is_valid_password(password):
    password_str = str(password)
    last_num = password_str[0]

    group_length = 1

    has_couple = False

    for cur_num in password_str[1:]:
        if int(last_num) > int(cur_num):
            return False
        if last_num == cur_num:
            group_length += 1
        else:
            if group_length == 2:
                has_couple = True
            last_num = cur_num
            group_length = 1
    if group_length == 2: # if the double is at the end
        has_couple = True
    return has_couple

n = 0
for cur_password in range(lower_bound, upper_bound + 1):
    if is_valid_password(cur_password):
        n += 1

print(n)