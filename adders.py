def make_adders(n):
    """Return a list of n functions where the i-th function adds i to its argument."""
    return [lambda x, i=i: x + i for i in range(n)]
