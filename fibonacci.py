#!/usr/bin/env python3
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <N>", file=sys.stderr)
        return 1

    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Error: N must be an integer.", file=sys.stderr)
        return 1

    if n < 0:
        print("Error: N must be non-negative.", file=sys.stderr)
        return 1

    a, b = 0, 1
    for _ in range(n):
        print(a)
        a, b = b, a + b

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
