from semver import SemVer

# Basic comparison
assert SemVer("1.0.0") > SemVer("0.9.9")
assert SemVer("2.0.0") > SemVer("1.9.9")
assert SemVer("1.1.0") > SemVer("1.0.9")
assert SemVer("1.0.0") == SemVer("1.0.0")

# Release > pre-release
assert SemVer("1.0.0") > SemVer("1.0.0-alpha")
assert SemVer("1.0.0") > SemVer("1.0.0-rc.1")

# Pre-release ordering (from semver.org spec)
versions = [
    "1.0.0-alpha",
    "1.0.0-alpha.1",
    "1.0.0-alpha.beta",
    "1.0.0-beta",
    "1.0.0-beta.2",
    "1.0.0-beta.11",   # numeric: 11 > 2, NOT lexicographic "11" < "2"
    "1.0.0-rc.1",
    "1.0.0",
]
parsed = [SemVer(v) for v in versions]
assert parsed == sorted(parsed), f"Wrong order: {[str(v) for v in sorted(parsed)]}"

# Numeric identifiers compared numerically, not lexicographically
assert SemVer("1.0.0-beta.11") > SemVer("1.0.0-beta.2")
assert SemVer("1.0.0-beta.9") < SemVer("1.0.0-beta.10")

# Numeric identifiers < alphanumeric identifiers
assert SemVer("1.0.0-1") < SemVer("1.0.0-alpha")
assert SemVer("1.0.0-alpha.1") < SemVer("1.0.0-alpha.beta")  # 1 (numeric) < beta (alpha)

# String representation roundtrip
assert str(SemVer("1.2.3-rc.1")) == "1.2.3-rc.1"
assert str(SemVer("1.0.0")) == "1.0.0"

print("ALL TESTS PASSED")
