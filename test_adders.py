from adders import make_adders

adders = make_adders(5)

assert adders[0](10) == 10, f"adders[0](10) should be 10, got {adders[0](10)}"
assert adders[1](10) == 11, f"adders[1](10) should be 11, got {adders[1](10)}"
assert adders[2](10) == 12, f"adders[2](10) should be 12, got {adders[2](10)}"
assert adders[3](10) == 13, f"adders[3](10) should be 13, got {adders[3](10)}"
assert adders[4](10) == 14, f"adders[4](10) should be 14, got {adders[4](10)}"

print("ALL TESTS PASSED")
