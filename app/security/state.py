from __future__ import annotations

import hashlib

from .models import User

_USERS: dict[str, User] = {
    "default": User(name="default", nopass=True),
}


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def get_user(name: str) -> User | None:
    return _USERS.get(name)


def list_usernames() -> list[str]:
    return sorted(_USERS.keys())


def set_user_rules(name: str, rules: list[str]) -> None:
    user = _USERS.get(name)
    if user is None:
        user = User(name=name, enabled=False, command_patterns=["-@all"],
                    key_patterns=set(), channel_patterns=set())
        _USERS[name] = user

    for rule in rules:
        if rule == "on":
            user.enabled = True
        elif rule == "off":
            user.enabled = False
        elif rule == "nopass":
            user.nopass = True
            user.password_hashes.clear()
        elif rule == "resetpass":
            user.nopass = False
            user.password_hashes.clear()
        elif rule == "reset":
            user.enabled = False
            user.nopass = False
            user.password_hashes.clear()
            user.command_patterns = ["-@all"]
            user.key_patterns.clear()
            user.channel_patterns.clear()
        elif rule.startswith(">"):
            user.nopass = False
            user.password_hashes.add(_hash_password(rule[1:]))
        elif rule.startswith("<"):
            user.password_hashes.discard(_hash_password(rule[1:]))
        elif rule.startswith(("+", "-")):
            user.command_patterns.append(rule)
        elif rule.startswith("~"):
            user.key_patterns.add(rule[1:])
        elif rule.startswith("&"):
            user.channel_patterns.add(rule[1:])
        else:
            raise ValueError(f"Invalid ACL rule: {rule!r}")


def delete_users(names: list[str]) -> int:
    count = 0
    for name in names:
        if name == "default":
            raise ValueError("The 'default' user cannot be removed")
        if _USERS.pop(name, None) is not None:
            count += 1
    return count


def reset_acl_state() -> None:
    _USERS.clear()
    _USERS["default"] = User(name="default", nopass=True)
