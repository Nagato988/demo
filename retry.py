#!/usr/bin/env python3

import time
from functools import wraps


def retry(max_attempts: int, delay: float = 0):
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exc = exc
                    if attempt < max_attempts - 1 and delay > 0:
                        time.sleep(delay)
            raise last_exc

        return wrapper

    return decorator
