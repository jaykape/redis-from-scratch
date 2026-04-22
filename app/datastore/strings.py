from __future__ import annotations

import time
from typing import Any

from app.state import EXPIRIES, STORE

from .expiry import expire_if_needed


def set_value(key: str, value: str, ex: int | None = None) -> None:
    STORE[key] = value
    if ex is not None:
        EXPIRIES[key] = time.time() + ex
    else:
        EXPIRIES.pop(key, None)


def get_value(key: str) -> Any:
    if expire_if_needed(key):
        return None
    return STORE.get(key)


def incr_value(key: str, by: int = 1) -> int:
    if expire_if_needed(key):
        pass
    val = STORE.get(key)
    if val is None:
        new_val = by
    else:
        try:
            new_val = int(val) + by
        except ValueError:
            raise ValueError("ERR value is not an integer or out of range")
    STORE[key] = str(new_val)
    return new_val
