with open("day7.txt") as f:
    puzzle_input = f.read().splitlines()

bags = {}

for line in puzzle_input:
    split = line.split(" contain ")
    bag_color = split[0][:-5]
    if split[1] == "no other bags.":
        bags[bag_color] = []
    else:
        bags[bag_color] = [(int(x[:2]), x[2:x.index(" bag")]) for x in split[1].split(", ")]

def sub_bags(bag):
    sub_colors = bags[bag]
    return sum([amount * (sub_bags(color) + 1) for amount, color in sub_colors])

print(sub_bags("shiny gold"))