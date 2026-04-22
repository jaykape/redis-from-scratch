from __future__ import annotations

from typing import TYPE_CHECKING

from .models import User
from .state import _USERS

if TYPE_CHECKING:
    from app.client.session import ClientSession

_ACL_CATEGORIES: dict[str, set[str]] = {
    "read": {"GET", "KEYS", "EXISTS", "TYPE", "TTL"},
    "write": {"SET", "DEL", "INCR", "DECR"},
    "string": {"GET", "SET", "INCR", "DECR"},
    "keyspace": {"DEL", "EXISTS", "KEYS", "TTL", "TYPE"},
    "server": {"CONFIG", "SELECT"},
    "connection": {"PING", "ECHO", "HELLO", "CLIENT", "QUIT"},
    "admin": {"ACL", "CONFIG", "SELECT"},
    "fast": {"GET", "INCR", "DECR", "PING", "SET"},
    "slow": {"CONFIG", "KEYS"},
}


def check_command_permission(session: "ClientSession", command: str) -> str | None:
    user = _USERS.get(session.auth_user or "default")
    if user is None:
        return f"NOPERM No permissions to run '{command.lower()}'"
    for rule in user.command_patterns:
        if rule in ("+@all", "allcommands"):
            return None
    return f"NOPERM this user has no permissions to run the '{command.lower()}' command"


def user_flags(user: User) -> list[str]:
    flags = ["on" if user.enabled else "off"]
    if user.nopass:
        flags.append("nopass")
    return flags


def command_rules(user: User) -> str:
    return " ".join(user.command_patterns)


def describe_user(user: User) -> list[object]:
    return [
        "flags", user_flags(user),
        "passwords", sorted(user.password_hashes),
        "commands", command_rules(user),
        "keys", list(user.key_patterns),
        "channels", list(user.channel_patterns),
    ]


def list_acl_categories(category: str | None = None) -> list[str]:
    if category is None:
        return sorted(f"@{cat}" for cat in _ACL_CATEGORIES)
    cat = category.lstrip("@").lower()
    if cat not in _ACL_CATEGORIES:
        raise ValueError(f"Unknown category '{category}'")
    return sorted(_ACL_CATEGORIES[cat])
