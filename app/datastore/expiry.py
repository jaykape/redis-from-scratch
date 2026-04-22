from __future__ import annotations

import time

from app.state import EXPIRIES, STORE


def now() -> float:
    return time.time()


def expire_if_needed(key: str) -> bool:
    expiry = EXPIRIES.get(key)
    if expiry is None:
        return False
    if expiry > now():
        return False
    STORE.pop(key, None)
    EXPIRIES.pop(key, None)
    return True


def get_ttl(key: str) -> int:
    if key not in STORE:
        return -2
    if expire_if_needed(key):
        return -2
    expiry = EXPIRIES.get(key)
    if expiry is None:
        return -1
    return max(0, int(expiry - now()))
