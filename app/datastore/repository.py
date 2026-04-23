from __future__ import annotations
from .expiry import expire_if_needed
from app.state import EXPIRIES, STORE
from .entry import Entry
from typing import Any
import time


def set_value(key: str, value: object, type_: str) -> None:
    STORE[key] = Entry(type_, value)


def set_expiry(key: str, ex: int | None) -> None:
    if ex is not None:
        EXPIRIES[key] = time.time() + ex
    else:
        EXPIRIES.pop(key, None)


def get_expiry(key: str) -> float | None:
    return EXPIRIES.get(key)


def get_value(key: str) -> tuple[object | None, str | None]:
    if expire_if_needed(key):
        return None, None
    entry = STORE.get(key)
    if entry is None:
        return None, None
    return entry.value, entry.type
