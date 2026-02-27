#!/usr/bin/env python3


def describe(data: list[float]) -> dict:
    n = len(data)
    if n == 0:
        raise ValueError("data must not be empty")

    sorted_data = sorted(data)
    mean = sum(data) / n

    if n % 2 == 1:
        median = sorted_data[n // 2]
    else:
        median = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2

    variance = sum((x - mean) ** 2 for x in data) / n
    std_dev = variance**0.5

    return {
        "count": n,
        "mean": mean,
        "median": median,
        "min": min(data),
        "max": max(data),
        "std_dev": std_dev,
    }
