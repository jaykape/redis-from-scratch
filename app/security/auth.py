from __future__ import annotations

from typing import TYPE_CHECKING

from .state import _USERS, _hash_password

if TYPE_CHECKING:
    from app.client.session import ClientSession


def default_user_nopass() -> bool:
    user = _USERS.get("default")
    return user is not None and user.nopass


def authenticate_session(session: "ClientSession", username: str, password: str) -> None:
    user = _USERS.get(username)
    if user is None or not user.enabled:
        raise ValueError("WRONGPASS invalid username-password pair or user is disabled.")
    if user.nopass:
        session.authenticated = True
        session.auth_user = username
        return
    if _hash_password(password) not in user.password_hashes:
        raise ValueError("WRONGPASS invalid username-password pair or user is disabled.")
    session.authenticated = True
    session.auth_user = username
