from __future__ import annotations

from typing import TYPE_CHECKING

from app import security
from app.client import resp

if TYPE_CHECKING:
    from app.client.session import ClientSession


async def handle_auth(args: list[str], session: "ClientSession") -> bytes:
    if len(args) not in {1, 2}:
        return resp.arity_error("auth")

    username = "default" if len(args) == 1 else args[0]
    password = args[-1]
    try:
        security.authenticate_session(session, username, password)
    except ValueError as exc:
        return resp.error(str(exc))
    return resp.simple_string("OK")


async def handle_acl(args: list[str], session: "ClientSession") -> bytes:
    if not args:
        return resp.arity_error("acl")

    sub = args[0].upper()
    if sub == "WHOAMI":
        return resp.bulk_string(session.auth_user or "default")
    if sub == "USERS":
        return resp.array(security.list_usernames())
    if sub == "LIST":
        return resp.array([
            security.describe_user(security.get_user(name))
            for name in security.list_usernames()
        ])
    if sub == "GETUSER":
        if len(args) != 2:
            return resp.arity_error("acl|getuser")
        user = security.get_user(args[1])
        if user is None:
            return resp.null_bulk()
        return resp.array([
            "flags", security.user_flags(user),
            "passwords", sorted(user.password_hashes),
            "commands", security.command_rules(user),
            "keys", list(user.key_patterns),
            "channels", list(user.channel_patterns),
        ])
    if sub == "SETUSER":
        if len(args) < 3:
            return resp.arity_error("acl|setuser")
        try:
            security.set_user_rules(args[1], args[2:])
        except ValueError as exc:
            return resp.error(f"ERR {exc}")
        return resp.simple_string("OK")
    if sub == "DELUSER":
        if len(args) < 2:
            return resp.arity_error("acl|deluser")
        return resp.integer(security.delete_users(args[1:]))
    if sub == "CAT":
        try:
            return resp.array(security.list_acl_categories(args[1] if len(args) == 2 else None))
        except ValueError as exc:
            return resp.error(f"ERR {exc}")

    return resp.error(f"ERR unknown subcommand '{args[0]}' for 'acl' command")
