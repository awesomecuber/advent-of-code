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
    while len(expression) >= 3:
        expression = [str(eval(expression[0] + expression[1] + expression[2]))] + expression[3:]
    return expression[0]

print(sum([int(evaluate_expression(x)) for x in puzzle_input]))