from __future__ import annotations

import contextvars
from collections.abc import MutableMapping
from typing import Any

from app.config import CONFIG, reset_config

NUM_DBS = int(CONFIG["databases"].value)
CURRENT_DB: contextvars.ContextVar[int] = contextvars.ContextVar(
    "app_current_db", default=0)

_STORES: list[dict[str, Any]] = [{} for _ in range(NUM_DBS)]
_EXPIRIES: list[dict[str, float]] = [{} for _ in range(NUM_DBS)]


class _DBProxy(MutableMapping):
    __slots__ = ("_backing",)

    def __init__(self, backing: list[dict[str, Any]]) -> None:
        self._backing = backing

    def _current(self) -> dict[str, Any]:
        return self._backing[CURRENT_DB.get()]

    def __getitem__(self, key):
        return self._current()[key]

    def __setitem__(self, key, value):
        self._current()[key] = value

    def __delitem__(self, key):
        del self._current()[key]

    def __iter__(self):
        return iter(self._current())

    def __len__(self):
        return len(self._current())

    def get(self, key, default=None):
        return self._current().get(key, default)

    def pop(self, key, *args):
        return self._current().pop(key, *args)

    def clear(self) -> None:
        self._current().clear()

    def items(self):
        return self._current().items()


STORE: MutableMapping = _DBProxy(_STORES)
EXPIRIES: MutableMapping = _DBProxy(_EXPIRIES)


def configure_state(num_dbs: int | None = None) -> None:
    global NUM_DBS, _STORES, _EXPIRIES

    count = num_dbs if num_dbs is not None else int(CONFIG["databases"].value)
    NUM_DBS = count
    _STORES = [{} for _ in range(NUM_DBS)]
    _EXPIRIES = [{} for _ in range(NUM_DBS)]
    STORE._backing = _STORES
    EXPIRIES._backing = _EXPIRIES
    CURRENT_DB.set(0)


def reset_state() -> None:
    """Reset in-memory server state and configuration to a clean baseline."""
    reset_config()
    configure_state()

    from app.security import reset_acl_state

    reset_acl_state()
