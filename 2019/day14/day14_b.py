from collections import Counter
import os
from pprint import pprint
import sys

with open(os.path.join(sys.path[0], "day14.txt")) as f:
    puzzle_input = f.read().splitlines()

TRILLION = 1000000000000

Ingredient = tuple[int, str]

to_make: dict[str, tuple[int, set[Ingredient]]] = {}

for line in puzzle_input:
    left, right = line.split(" => ")
    ingredient_strs = left.split(", ")
    ingredients: set[Ingredient] = set()
    for ingredient_str in ingredient_strs:
        quantity, chemical = ingredient_str.split()
        ingredients.add((int(quantity), chemical))
    quantity, chemical = right.split()
    to_make[chemical] = (int(quantity), ingredients)


def get_requirements(
    source_quantity: int, source_chemical: str, leftovers: Counter[str] = None
):
    if leftovers is None:
        leftovers = Counter()

    if source_chemical == "ORE":
        return source_quantity
    recipe_quantity, ingredients = to_make[source_chemical]
    times_to_run_reaction = ((source_quantity - 1) // recipe_quantity) + 1
    excess = (recipe_quantity * times_to_run_reaction) - source_quantity
    fuel_needed = 0
    for quantity, chemical in ingredients:
        adjusted_quantity = times_to_run_reaction * quantity
        use_from_leftovers = min(adjusted_quantity, leftovers[chemical])
        fuel_needed += get_requirements(
            adjusted_quantity - use_from_leftovers, chemical, leftovers
        )
        leftovers[chemical] -= use_from_leftovers
    leftovers[source_chemical] += excess
    return fuel_needed


# -1 if not enough fuel
# 1 if too much fuel
# 0 if just right
def is_correct_fuel(fuel_amount: int) -> int:
    if get_requirements(fuel_amount, "FUEL") > TRILLION:
        return 1
    if get_requirements(fuel_amount + 1, "FUEL") <= TRILLION:
        return -1
    return 0


ore_per_fuel = get_requirements(1, "FUEL")
lower_bound = TRILLION // ore_per_fuel
upper_bound = TRILLION

while True:
    guess = (lower_bound + upper_bound) // 2
    guess_result = is_correct_fuel(guess)
    if guess_result == -1:
        lower_bound = guess
    elif guess_result == 1:
        upper_bound = guess
    else:
        break

print(guess)
