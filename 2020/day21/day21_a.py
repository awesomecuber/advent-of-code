import itertools
import os
import pprint
import sys

with open(os.path.join(sys.path[0], "day21.txt")) as f:
    puzzle_input = f.read().splitlines()

all_ingredients = set()
all_allergens = set()
foods = []

for line in puzzle_input:
    food_ingredients, food_allergens = line.split(' (contains ')
    food_ingredients = set(food_ingredients.split())
    food_allergens = set(food_allergens[:-1].split(', '))
    all_ingredients |= food_ingredients
    all_allergens |= food_allergens
    foods.append((food_ingredients, food_allergens))

can_be = {k: {k2: False for k2 in all_allergens} for k in all_ingredients}

allergen_possible_ingredients = {k: set(all_ingredients) for k in all_allergens}

for ingredients, allergens in foods:
    for allergen in allergens:
        allergen_possible_ingredients[allergen] &= ingredients

for allergen, ingredients in allergen_possible_ingredients.items():
    for ingredient in ingredients:
        can_be[ingredient][allergen] = True

no_allergen_ingredients = set()
for ingredient, allergens in can_be.items():
    if not any(allergens.values()):
        no_allergen_ingredients.add(ingredient)

no_allergen_count = 0
for ingredients, _ in foods:
    for ingredient in ingredients:
        if ingredient in no_allergen_ingredients:
            no_allergen_count += 1
print(no_allergen_count)