#!/usr/bin/env python3
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file_path>", file=sys.stderr)
        return 1

    file_path = Path(sys.argv[1])

    try:
        content = file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: file not found: {file_path}", file=sys.stderr)
        return 1

    lines = content.count("\n")
    if content and not content.endswith("\n"):
        lines += 1

    words = len(content.split())
    chars = len(content)

    print(f"lines: {lines}")
    print(f"words: {words}")
    print(f"chars: {chars}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
