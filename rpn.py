#!/usr/bin/env python3


def evaluate(expression: str) -> float:
    stack = []

    for token in expression.split():
        if token in {"+", "-", "*", "/"}:
            if len(stack) < 2:
                raise ValueError("Invalid RPN expression")
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            else:
                stack.append(a / b)
        else:
            stack.append(float(token))

    if len(stack) != 1:
        raise ValueError("Invalid RPN expression")

    return float(stack[0])
