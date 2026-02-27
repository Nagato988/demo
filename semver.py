"""Semantic version parsing and comparison."""

from __future__ import annotations

import re
from functools import total_ordering

_SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)


@total_ordering
class SemVer:
    def __init__(self, version_str: str) -> None:
        match = _SEMVER_RE.match(version_str)
        if not match:
            raise ValueError(f"Invalid semantic version: {version_str}")

        self._original = version_str
        self.major = int(match.group(1))
        self.minor = int(match.group(2))
        self.patch = int(match.group(3))
        prerelease = match.group(4)
        self.prerelease = tuple(prerelease.split(".")) if prerelease else ()

    def __str__(self) -> str:
        return self._original

    def __repr__(self) -> str:
        return f"SemVer({self._original!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SemVer):
            return NotImplemented
        return self._cmp_tuple() == other._cmp_tuple()

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, SemVer):
            return NotImplemented

        left_base = (self.major, self.minor, self.patch)
        right_base = (other.major, other.minor, other.patch)
        if left_base != right_base:
            return left_base < right_base

        return self._prerelease_lt(other)

    def _cmp_tuple(self):
        return (self.major, self.minor, self.patch, self.prerelease)

    def _prerelease_lt(self, other: "SemVer") -> bool:
        # A release version has higher precedence than any prerelease version.
        if not self.prerelease and not other.prerelease:
            return False
        if not self.prerelease:
            return False
        if not other.prerelease:
            return True

        for a, b in zip(self.prerelease, other.prerelease):
            if a == b:
                continue
            a_num = a.isdigit()
            b_num = b.isdigit()

            if a_num and b_num:
                return int(a) < int(b)
            if a_num != b_num:
                # Numeric identifiers always have lower precedence.
                return a_num
            return a < b

        # If all compared identifiers are equal, shorter set has lower precedence.
        return len(self.prerelease) < len(other.prerelease)
