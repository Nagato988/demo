#!/usr/bin/env python3

from urllib.parse import parse_qsl, urlsplit


def parse_url(url: str) -> dict:
    parts = urlsplit(url)
    return {
        "scheme": parts.scheme or None,
        "host": parts.hostname,
        "port": parts.port,
        "path": parts.path,
        "query": dict(parse_qsl(parts.query, keep_blank_values=True)),
        "fragment": parts.fragment or None,
    }
