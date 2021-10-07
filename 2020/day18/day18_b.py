import os
import sys

with open(os.path.join(sys.path[0], "day18.txt")) as f:
    puzzle_input = f.read().splitlines()

def evaluate_expression(expression):
    while expression.find("(") != -1:
        left = expression.find("(")
        depth = 1
        right = left
        while depth != 0:
            right += 1
            character = expression[right]
            if character == ")":
                depth -= 1
            elif character == "(":
                depth += 1
        expression = expression[:left] + evaluate_expression(expression[left + 1:right]) + expression[right + 1:]
    expression = expression.split(" ")
    while len([x for x in expression if x == "+"]) > 0:
        plus_location = expression.index("+")
        the_sum = int(expression[plus_location - 1]) + int(expression[plus_location + 1])
        expression[plus_location - 1:plus_location + 2] = [str(the_sum)]
    return str(eval("".join(expression)))

print(sum([int(evaluate_expression(x)) for x in puzzle_input]))