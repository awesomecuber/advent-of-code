import time, math, itertools

coins = [1, 5, 10, 25]

calculated = {}
def get_combinations(total):
    if total == 0:
        return set()
    to_return = set()
    for coin in coins:
        if total - coin >= 0:
            if total - coin not in calculated:
                calculated[total - coin] = get_combinations(total - coin)
            sub_combinations = calculated[total - coin]
            for sub_combination in sub_combinations:
                to_return.add(tuple(sorted([coin] + list(sub_combination))))
            if len(sub_combinations) == 0:
                to_return.add((coin,))
    return to_return

def get_combinations2(total):
    counter = 0
    num_of_coins = [math.ceil(total / coins[i]) + 1 for i in range(len(coins))]
    for coin_counts in itertools.product(*[range(x) for x in num_of_coins]):
        if sum([coin_counts[i] * coins[i] for i in range(len(coins))]) == total:
            counter += 1
    return counter

def get_combinations3(total):
    arr = [[0 for _ in range(total + 1)] for _ in range(len(coins))]
    arr[0][0] = 1 # one way to make 0 total with only lowest coin
    for num_coins in range(0, len(coins)):
        for cur_total in range(0, total + 1):
            if cur_total - coins[num_coins] >= 0:
                # use our biggest coin
                arr[num_coins][cur_total] += arr[num_coins][cur_total - coins[num_coins]]
            if num_coins > 0:
                # don't use our biggest coin
                arr[num_coins][cur_total] += arr[num_coins - 1][cur_total]
    return arr[len(coins) - 1][total]

print("nico!")
print()

start_time = time.time()
answer = len(get_combinations(50))
print("50:", answer, time.time() - start_time)

start_time = time.time()
answer = len(get_combinations(100))
print("100:", answer, time.time() - start_time)

start_time = time.time()
answer = len(get_combinations(150))
print("150:", answer, time.time() - start_time)

start_time = time.time()
answer = len(get_combinations(200))
print("200:", answer, time.time() - start_time)

start_time = time.time()
answer = len(get_combinations(250))
print("250:", answer, time.time() - start_time)

print()
print("dad!")
print()

start_time = time.time()
answer = get_combinations2(50)
print("50:", answer, time.time() - start_time)

start_time = time.time()
answer = get_combinations2(100)
print("100:", answer, time.time() - start_time)

start_time = time.time()
answer = get_combinations2(150)
print("150:", answer, time.time() - start_time)

start_time = time.time()
answer = get_combinations2(200)
print("200:", answer, time.time() - start_time)

start_time = time.time()
answer = get_combinations2(250)
print("250:", answer, time.time() - start_time)

print()
print("new nico!")
print()

start_time = time.time()
answer = get_combinations3(50)
print("50:", answer, time.time() - start_time)

start_time = time.time()
answer = get_combinations3(100)
print("100:", answer, time.time() - start_time)

start_time = time.time()
answer = get_combinations3(150)
print("150:", answer, time.time() - start_time)

start_time = time.time()
answer = get_combinations3(200)
print("200:", answer, time.time() - start_time)

start_time = time.time()
answer = get_combinations3(250)
print("250:", answer, time.time() - start_time)
