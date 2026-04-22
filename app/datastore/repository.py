from __future__ import annotations
from .expiry import expire_if_needed
from app.state import EXPIRIES, STORE
from typing import Any
import time


def incr_value(key: str, by: int = 1) -> int:
    if expire_if_needed(key):
        value, type_ = None, None
    else:
        entry = STORE.get(key)
        if entry is None:
            value, type_ = None, None
        else:
            value, type_ = entry["value"], entry["type"]
    if value is None:
        new_val = by
    else:
        if type_ != "string":
            raise ValueError(
                "WRONGTYPE Operation against a key holding the wrong kind of value")
        try:
            new_val = int(value) + by
        except (ValueError, TypeError):
            raise ValueError("ERR value is not an integer or out of range")
    STORE[key] = {"type": "string", "value": str(new_val)}
    return new_val


def set_value(key: str, value: object, type_: str) -> None:
    STORE[key] = {"type": type_, "value": value}


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
    return entry["value"], entry["type"]
