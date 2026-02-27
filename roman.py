#!/usr/bin/env python3

_ROMAN_PAIRS = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]

_ROMAN_VALUES = {symbol: value for value, symbol in _ROMAN_PAIRS}


def to_roman(n: int) -> str:
    if not 1 <= n <= 3999:
        raise ValueError("n must be in range 1..3999")

    parts = []
    remaining = n
    for value, symbol in _ROMAN_PAIRS:
        count, remaining = divmod(remaining, value)
        parts.append(symbol * count)
    return "".join(parts)


def from_roman(s: str) -> int:
    if not s:
        raise ValueError("Roman numeral must be non-empty")

    i = 0
    total = 0
    while i < len(s):
        if i + 1 < len(s) and s[i : i + 2] in _ROMAN_VALUES:
            total += _ROMAN_VALUES[s[i : i + 2]]
            i += 2
        elif s[i] in _ROMAN_VALUES:
            total += _ROMAN_VALUES[s[i]]
            i += 1
        else:
            raise ValueError(f"Invalid Roman numeral: {s}")

    if not 1 <= total <= 3999 or to_roman(total) != s:
        raise ValueError(f"Invalid Roman numeral: {s}")

    return total
