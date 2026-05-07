# Server commands
from __future__ import annotations
from app import state
from app.client import resp
from app.config import CONFIG, set_config_value
async def handle_acl(args, session): pass
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
