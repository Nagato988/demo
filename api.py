#!/usr/bin/env python3
"""Simple HTTP API server with /healthz endpoint and rate limiting."""

import json
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

# ── Config ────────────────────────────────────────────────────────────────────

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

def load_version() -> str:
    try:
        with open(CONFIG_PATH) as f:
            return json.load(f).get("version", "unknown")
    except (FileNotFoundError, json.JSONDecodeError):
        return "unknown"

# ── Rate limiter ──────────────────────────────────────────────────────────────

RATE_LIMIT = 60          # requests
RATE_WINDOW = 60         # seconds

_rate_lock = threading.Lock()
_rate_buckets: dict[str, list[float]] = {}  # ip -> list of timestamps


def is_rate_limited(ip: str) -> tuple[bool, int]:
    """Returns (limited, retry_after_seconds)."""
    now = time.time()
    with _rate_lock:
        timestamps = _rate_buckets.get(ip, [])
        # Drop timestamps outside the window
        timestamps = [t for t in timestamps if now - t < RATE_WINDOW]
        if len(timestamps) >= RATE_LIMIT:
            oldest = timestamps[0]
            retry_after = int(RATE_WINDOW - (now - oldest)) + 1
            _rate_buckets[ip] = timestamps
            return True, retry_after
        timestamps.append(now)
        _rate_buckets[ip] = timestamps
        return False, 0

# ── Request handler ───────────────────────────────────────────────────────────

class APIHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass  # suppress default access log

    def get_client_ip(self) -> str:
        forwarded = self.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return self.client_address[0]

    def send_json(self, status: int, body: dict, extra_headers: dict | None = None):
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, str(v))
        self.end_headers()
        self.wfile.write(payload)

    def check_rate_limit(self) -> bool:
        """Returns True if request should be blocked. Sends 429 response."""
        ip = self.get_client_ip()
        limited, retry_after = is_rate_limited(ip)
        if limited:
            self.send_json(
                429,
                {"error": "Too Many Requests"},
                {"Retry-After": retry_after},
            )
            return True
        return False

    def do_GET(self):
        if self.check_rate_limit():
            return

        if self.path == "/healthz":
            self.send_json(200, {"status": "ok", "version": load_version()})
        else:
            self.send_json(404, {"error": "Not Found"})


def make_server(host: str = "127.0.0.1", port: int = 8080) -> HTTPServer:
    return HTTPServer((host, port), APIHandler)


if __name__ == "__main__":
    server = make_server()
    print(f"Listening on http://127.0.0.1:8080")
    server.serve_forever()
