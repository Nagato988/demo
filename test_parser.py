from parser import parse_expr

# Basic arithmetic
assert parse_expr("2 + 3") == 5
assert parse_expr("10 - 4") == 6
assert parse_expr("3 * 4") == 12
assert parse_expr("10 / 4") == 2.5

# Operator precedence (no parens)
assert parse_expr("2 + 3 * 4") == 14       # not 20
assert parse_expr("10 - 2 * 3") == 4       # not 24
assert parse_expr("8 / 2 + 1") == 5.0      # not 2.666

# Parentheses override precedence
assert parse_expr("(2 + 3) * 4") == 20
assert parse_expr("(10 - 2) * (3 + 1)") == 32

# Exponentiation (right-associative)
assert parse_expr("2 ** 3") == 8
assert parse_expr("2 ** 3 ** 2") == 512    # 2**(3**2), not (2**3)**2

# Unary minus
assert parse_expr("-3 + 5") == 2
assert parse_expr("-(2 + 3)") == -5
assert parse_expr("2 * -3") == -6

# Floats
assert parse_expr("1.5 * 2") == 3.0

# Whitespace variations
assert parse_expr("2+3") == 5
assert parse_expr("  2  +  3  ") == 5

print("ALL TESTS PASSED")
