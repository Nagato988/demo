#!/usr/bin/env python3


def is_anagram(s1: str, s2: str) -> bool:
    normalized1 = sorted(ch.lower() for ch in s1 if ch != " ")
    normalized2 = sorted(ch.lower() for ch in s2 if ch != " ")
    return normalized1 == normalized2
