"""Utilities for flattening nested Python containers."""

from __future__ import annotations


def flatten(obj) -> list:
    """Recursively flatten lists, tuples, and sets into a single list.

    - Preserves ``None`` as a regular value.
    - Raises ``ValueError`` when a circular reference is detected.
    """

    result = []
    active_ids = set()

    def _walk(value):
        if isinstance(value, (list, tuple, set)):
            obj_id = id(value)
            if obj_id in active_ids:
                raise ValueError("Circular reference detected")

            active_ids.add(obj_id)
            try:
                for item in value:
                    _walk(item)
            finally:
                active_ids.remove(obj_id)
        else:
            result.append(value)

    _walk(obj)
    return result
