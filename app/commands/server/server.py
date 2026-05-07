# Server commands
from __future__ import annotations
from app import state
from app.client import resp
from app.config import CONFIG, set_config_value

from typing import TYPE_CHECKING

from app import security
from app.client import resp

if TYPE_CHECKING:
    from app.client.session import ClientSession


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


async def handle_config(args, session): pass
async def handle_dbszize(args, session): pass
async def handle_flushall(args, session): pass
async def handle_flushdb(args, session): pass
async def handle_info(args, session): pass
async def handle_lastsave(args, session): pass
async def handle_save(args, session): pass
async def handle_shutdown(args, session): pass


async def handle_select(args: list[str], session) -> bytes:
    if len(args) != 1:
        return resp.arity_error("select")
    try:
        db = int(args[0])
    except ValueError:
        return resp.error("ERR value is not an integer or out of range")
    if db < 0 or db >= state.NUM_DBS:
        return resp.error("ERR DB index is out of range")
    session.db = db
    return resp.simple_string("OK")


async def handle_config(args: list[str], session) -> bytes:
    if not args:
        return resp.arity_error("config")

    sub = args[0].upper()
    if sub == "GET":
        if len(args) < 2:
            return resp.arity_error("config|get")
        import fnmatch
        pairs: list[object] = []
        for pattern in args[1:]:
            for config_key, entry in CONFIG.items():
                if fnmatch.fnmatch(config_key, pattern.lower()):
                    pairs.append(config_key)
                    pairs.append(entry.value)
        return resp.array(pairs)

    if sub == "SET":
        if len(args) != 3:
            return resp.arity_error("config|set")
        key = args[1].lower()
        try:
            set_config_value(key, args[2])
        except KeyError:
            return resp.error(
                f"ERR CONFIG SET failed (possibly related to argument '{key}') - unknown option"
            )
        except PermissionError:
            return resp.error(
                f"ERR CONFIG SET failed (possibly related to argument '{key}') - can't set immutable config"
            )
        except ValueError as exc:
            return resp.error(
                f"ERR CONFIG SET failed (possibly related to argument '{key}') - {exc}"
            )
        return resp.simple_string("OK")

    return resp.error("ERR unsupported CONFIG subcommand")
