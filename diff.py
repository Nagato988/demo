#!/usr/bin/env python3

import difflib


def unified_diff(a: str, b: str, filename_a: str = 'a', filename_b: str = 'b') -> str:
    a_lines = a.splitlines(keepends=True)
    b_lines = b.splitlines(keepends=True)
    return ''.join(
        difflib.unified_diff(
            a_lines,
            b_lines,
            fromfile=filename_a,
            tofile=filename_b,
            lineterm='\n',
        )
    )
