#!/usr/bin/env python3


def parse(text: str) -> dict:
    result = {}
    current = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip()
            if not section:
                raise ValueError("Empty section name")
            result.setdefault(section, {})
            current = result[section]
            continue

        if "=" in line:
            if current is None:
                raise ValueError("Key-value pair outside any section")
            key, value = line.split("=", 1)
            current[key.strip()] = value.strip()
            continue

        raise ValueError(f"Invalid INI line: {raw_line}")

    return result


def dumps(data: dict) -> str:
    lines = []
    first = True

    for section, values in data.items():
        if not first:
            lines.append("")
        first = False

        lines.append(f"[{section}]")
        for key, value in values.items():
            lines.append(f"{key} = {value}")

    return "\n".join(lines) + ("\n" if lines else "")
