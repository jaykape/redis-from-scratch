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
    entry = STORE.get(key)
    return entry is not None


def type_of(key: str) -> str:
    if expire_if_needed(key):
        return "none"
    entry = STORE.get(key)
    if entry is None:
        return "none"
    if isinstance(entry, dict) and "type" in entry:
        return entry["type"]
    if isinstance(entry, str):
        return "string"
    return "unknown"


def keys_matching(pattern: str) -> list[str]:
    all_keys = list(STORE.keys())
    return [k for k in all_keys if not expire_if_needed(k) and fnmatch.fnmatch(k, pattern)]
