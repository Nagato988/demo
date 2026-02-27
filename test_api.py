"""Tests for api.py — /healthz endpoint and rate limiting."""

import json
import threading
import time
import urllib.request
import urllib.error

from api import make_server, RATE_LIMIT, RATE_WINDOW, _rate_buckets, _rate_lock

PORT = 18080
BASE = f"http://127.0.0.1:{PORT}"


def setup_server():
    server = make_server("127.0.0.1", PORT)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    time.sleep(0.1)
    return server


def get(path, headers=None):
    req = urllib.request.Request(f"{BASE}{path}", headers=headers or {})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read()), dict(resp.headers)
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read()), dict(e.headers)


def clear_rate_buckets():
    with _rate_lock:
        _rate_buckets.clear()


# ── Tests ─────────────────────────────────────────────────────────────────────

def test_healthz_returns_200():
    status, body, _ = get("/healthz")
    assert status == 200, f"Expected 200, got {status}"
    assert body["status"] == "ok", f"Expected status=ok, got {body}"
    assert "version" in body, "Missing 'version' field"
    print("  PASS: /healthz returns 200 with status and version")


def test_healthz_version_matches_config():
    import json as _json, os
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path) as f:
        expected_version = _json.load(f)["version"]
    _, body, _ = get("/healthz")
    assert body["version"] == expected_version, f"Version mismatch: {body['version']} != {expected_version}"
    print(f"  PASS: /healthz version matches config.json ({expected_version})")


def test_rate_limit_returns_429():
    clear_rate_buckets()
    # Exhaust the limit
    for _ in range(RATE_LIMIT):
        get("/healthz")
    # Next request should be 429
    status, body, headers = get("/healthz")
    assert status == 429, f"Expected 429, got {status}"
    assert "Retry-After" in headers, "Missing Retry-After header"
    retry_after = int(headers["Retry-After"])
    assert 0 < retry_after <= RATE_WINDOW + 1, f"Retry-After out of range: {retry_after}"
    print(f"  PASS: rate limit returns 429 after {RATE_LIMIT} requests (Retry-After: {retry_after}s)")


def test_404_for_unknown_path():
    clear_rate_buckets()
    status, body, _ = get("/unknown")
    assert status == 404, f"Expected 404, got {status}"
    print("  PASS: unknown path returns 404")


if __name__ == "__main__":
    print("Starting test server...")
    server = setup_server()
    print(f"Server running on {BASE}\n")

    tests = [
        test_healthz_returns_200,
        test_healthz_version_matches_config,
        test_rate_limit_returns_429,
        test_404_for_unknown_path,
    ]

    passed = failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  FAIL: {test.__name__}: {e}")
            failed += 1

    server.shutdown()
    print(f"\n{passed} passed, {failed} failed")
    exit(failed)
