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
    food_ingredients, food_allergens = line.split(" (contains ")
    food_ingredients = set(food_ingredients.split())
    food_allergens = set(food_allergens[:-1].split(", "))
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

for ingredient in no_allergen_ingredients:
    del can_be[ingredient]


def get_true(dict):
    return [k for k, v in dict.items() if v]


answer = {k: "" for k in can_be}

we_done = False
while not we_done:
    we_done = True
    for ingredient, truth_table in can_be.items():
        possible_allergens = get_true(truth_table)
        if len(possible_allergens) == 1:
            answer[ingredient] = possible_allergens[0]
            for ingredient2 in answer:
                can_be[ingredient2][possible_allergens[0]] = False
        elif len(possible_allergens) >= 1:
            we_done = False

almost_final_answer = sorted(list(answer.items()), key=lambda x: x[1])
print(",".join(x[0] for x in almost_final_answer))
