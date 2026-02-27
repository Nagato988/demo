#!/usr/bin/env python3


def add(a, b):
    return [[x + y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def subtract(a, b):
    return [[x - y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(a, b)]


def multiply(a, b):
    b_t = transpose(b)
    return [[sum(x * y for x, y in zip(row_a, col_b)) for col_b in b_t] for row_a in a]


def transpose(m):
    return [list(row) for row in zip(*m)]
