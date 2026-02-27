from flatten import flatten

# Basic
assert flatten([1, [2, 3], [4, [5]]]) == [1, 2, 3, 4, 5]

# None preserved
assert flatten([1, None, [2, None]]) == [1, None, 2, None]

# Tuples and sets treated as sequences
assert flatten([(1, 2), {3}]) == [1, 2, 3]

# Already flat
assert flatten([1, 2, 3]) == [1, 2, 3]

# Empty
assert flatten([]) == []

# Deep nesting
assert flatten([[[[[1]]]]]) == [1]

# Circular reference raises ValueError
a = [1, 2]
a.append(a)
try:
    flatten(a)
    assert False, "Should have raised ValueError"
except ValueError:
    pass

print("ALL TESTS PASSED")
