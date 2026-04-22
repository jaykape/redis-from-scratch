from __future__ import annotations

import fnmatch

from app.state import EXPIRIES, STORE

from .expiry import expire_if_needed


def del_value(key: str) -> bool:
    existed = key in STORE
    STORE.pop(key, None)
    EXPIRIES.pop(key, None)
    return existed


def exists(key: str) -> bool:
    if expire_if_needed(key):
        return False
    return key in STORE


def type_of(key: str) -> str:
    if expire_if_needed(key):
        return "none"
    value = STORE.get(key)
    if value is None:
        return "none"
    if isinstance(value, str):
        return "string"
    return "unknown"


def keys_matching(pattern: str) -> list[str]:
    all_keys = list(STORE.keys())
    return [k for k in all_keys if not expire_if_needed(k) and fnmatch.fnmatch(k, pattern)]
