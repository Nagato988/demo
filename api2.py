#!/usr/bin/env python3
"""HTTP API server with /healthz and per-IP sliding-window rate limiting."""

from __future__ import annotations

import json
import math
import os
import threading
import time
from collections import defaultdict, deque
from http.server import BaseHTTPRequestHandler, HTTPServer

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
LIMIT_PER_MINUTE = 60
WINDOW_SECONDS = 60


class SlidingWindowLimiter:
    def __init__(self, limit: int, window_seconds: int) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self._hits: dict[str, deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def check(self, key: str) -> tuple[bool, int]:
        now = time.time()
        with self._lock:
            window = self._hits[key]
            cutoff = now - self.window_seconds
            while window and window[0] <= cutoff:
                window.popleft()

            if len(window) >= self.limit:
                retry_after = max(1, math.ceil(self.window_seconds - (now - window[0])))
                return True, retry_after

            window.append(now)
            return False, 0


_limiter = SlidingWindowLimiter(LIMIT_PER_MINUTE, WINDOW_SECONDS)


def _version_from_config() -> str:
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return "unknown"

    version = data.get("version", "unknown")
    return version if isinstance(version, str) else "unknown"


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        # Keep test output clean.
        return

    def _client_ip(self) -> str:
        xff = self.headers.get("X-Forwarded-For")
        if xff:
            return xff.split(",", 1)[0].strip()
        return self.client_address[0]

    def _write_json(self, status_code: int, payload: dict, headers: dict | None = None) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        if headers:
            for name, value in headers.items():
                self.send_header(name, str(value))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        limited, retry_after = _limiter.check(self._client_ip())
        if limited:
            self._write_json(429, {"error": "Too Many Requests"}, {"Retry-After": retry_after})
            return

        if self.path == "/healthz":
            self._write_json(200, {"status": "ok", "version": _version_from_config()})
            return

        self._write_json(404, {"error": "Not Found"})


def make_server(host: str = "127.0.0.1", port: int = 8080) -> HTTPServer:
    return HTTPServer((host, port), Handler)


if __name__ == "__main__":
    srv = make_server()
    print("Listening on http://127.0.0.1:8080")
    srv.serve_forever()
