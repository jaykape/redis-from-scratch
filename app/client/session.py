from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from app.security import default_user_nopass


@dataclass
class ClientSession:
    client_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    db: int = 0
    authenticated: bool = field(default_factory=default_user_nopass)
    auth_user: str = "default"
    client_name: Optional[str] = None
    client_library_name: Optional[str] = None
    client_library_version: Optional[str] = None
    resp_version: int = 2
    closed: bool = False
