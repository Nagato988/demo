#!/usr/bin/env python3


def tokenize(text: str):
    tokens = []
    i = 0
    n = len(text)

    while i < n:
        ch = text[i]

        if ch.isspace():
            i += 1
            continue

        if ch == '(':
            tokens.append(("LPAREN", ch))
            i += 1
            continue

        if ch == ')':
            tokens.append(("RPAREN", ch))
            i += 1
            continue

        if ch in "+-*/=<>!":
            tokens.append(("OP", ch))
            i += 1
            continue

        if ch == '"':
            start = i
            i += 1
            value_chars = []
            while i < n:
                curr = text[i]
                if curr == '\\' and i + 1 < n:
                    value_chars.append(text[i + 1])
                    i += 2
                    continue
                if curr == '"':
                    i += 1
                    tokens.append(("STRING", ''.join(value_chars)))
                    break
                value_chars.append(curr)
                i += 1
            else:
                raise ValueError(f"Unterminated string starting at position {start}")
            continue

        if ch.isdigit():
            start = i
            while i < n and text[i].isdigit():
                i += 1
            tokens.append(("NUMBER", text[start:i]))
            continue

        if ch.isalpha() or ch == '_':
            start = i
            while i < n and (text[i].isalnum() or text[i] == '_'):
                i += 1
            tokens.append(("IDENT", text[start:i]))
            continue

        raise ValueError(f"Unexpected character at position {i}: {ch!r}")

    return tokens
