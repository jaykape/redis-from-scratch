from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Callable

from .validators import validate_yes_no, validate_non_empty

ConfigValidator = Callable[[str], str]


@dataclass(frozen=True)
class ConfigEntry:
    value: str
    mutable: bool
    validator: ConfigValidator | None = None


DEFAULT_CONFIG: dict[str, ConfigEntry] = {
    "bind": ConfigEntry(value="127.0.0.1", mutable=False, validator=validate_non_empty),
    "port": ConfigEntry(value="6379", mutable=False),
    "databases": ConfigEntry(value="16", mutable=False),
    "appendonly": ConfigEntry(value="no", mutable=True, validator=validate_yes_no),
    "appendfilename": ConfigEntry(value="appendonly.aof", mutable=True, validator=validate_non_empty),
    "dir": ConfigEntry(value="", mutable=True),
}

CONFIG: dict[str, ConfigEntry] = DEFAULT_CONFIG.copy()


def load_config_file(path: str) -> None:
    """Load a minimal Redis-style config file of `key value` pairs."""
    with open(path, "r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split(None, 1)
            if len(parts) != 2:
                raise ValueError(
                    f"Invalid config line {line_number}: expected '<key> <value>'"
                )

            key, value = parts[0].lower(), parts[1].strip()
            set_startup_config(key, value)


def set_startup_config(key: str, value: str) -> None:
    """Called by _parse_args at startup; validates but allows setting immutable keys."""
    entry = CONFIG.get(key)
    if entry is None:
        raise KeyError(key)

    validated_value = entry.validator(
        value) if entry.validator is not None else value
    CONFIG[key] = ConfigEntry(value=validated_value,
                              mutable=entry.mutable, validator=entry.validator)


def set_config_value(key: str, value: str) -> None:
    """Called by command `SET CONFIG`"""
    entry = CONFIG.get(key)
    if entry is None:
        raise KeyError(key)
    if not entry.mutable:
        raise PermissionError(key)

    validated_value = entry.validator(
        value) if entry.validator is not None else value
    CONFIG[key] = ConfigEntry(value=validated_value,
                              mutable=entry.mutable, validator=entry.validator)


def reset_config() -> None:
    """Restore runtime configuration values to their defaults."""
    CONFIG.clear()
    CONFIG.update(DEFAULT_CONFIG)
