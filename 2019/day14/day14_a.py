from collections import Counter
import os
from pprint import pprint
import sys

with open(os.path.join(sys.path[0], "day14.txt")) as f:
    puzzle_input = f.read().splitlines()

Ingredient = tuple[int, str]

to_make: dict[str, tuple[int, set[Ingredient]]] = {}

for line in puzzle_input:
    left, right = line.split(' => ')
    ingredient_strs = left.split(', ')
    ingredients: set[Ingredient] = set()
    for ingredient_str in ingredient_strs:
        quantity, chemical = ingredient_str.split()
        ingredients.add((int(quantity), chemical))
    quantity, chemical = right.split()
    to_make[chemical] = (int(quantity), ingredients)


def get_requirements(source_quantity: int, source_chemical: str, leftovers: Counter):
    if source_chemical == 'ORE':
        return source_quantity
    recipe_quantity, ingredients = to_make[source_chemical]
    times_to_run_reaction = ((source_quantity - 1) // recipe_quantity) + 1
    excess = (recipe_quantity * times_to_run_reaction) - source_quantity
    fuel_needed = 0
    for _ in range(times_to_run_reaction):
        for quantity, chemical in ingredients:
            use_from_leftovers = min(quantity, leftovers[chemical])
            fuel_needed += get_requirements(quantity - use_from_leftovers, chemical, leftovers)
            leftovers[chemical] -= use_from_leftovers
    leftovers[source_chemical] += excess
    return fuel_needed

pprint(get_requirements(1, 'FUEL', Counter()))
# leftovers: Counter = Counter()
# pprint(get_requirements(7, 'A', leftovers))
# pprint(leftovers)