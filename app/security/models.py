from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class User:
    name: str
    enabled: bool = True
    nopass: bool = False
    password_hashes: set[str] = field(default_factory=set)
    command_patterns: list[str] = field(default_factory=lambda: ["+@all"])
    key_patterns: set[str] = field(default_factory=lambda: {"*"})
    channel_patterns: set[str] = field(default_factory=lambda: {"*"})
