from __future__ import annotations

from app.client import resp
from app.datastore.repository import get_value, set_value, incr_value


async def handle_append(args: list[str], session) -> bytes:
    if len(args) != 2:
        return resp.arity_error("append")
    key, append_value = args[0], args[1]
    value, type_ = get_value(key)
    if value is not None and type_ != "string":
        return resp.error("WRONGTYPE Operation against a key holding the wrong kind of value")
    if value is None:
        set_value(key, append_value, "string")
        return resp.integer(len(append_value))
    else:
        set_value(key, value + append_value, "string")
        return resp.integer(len(value) + len(append_value))


async def handle_set(args: list[str], session) -> bytes:
    if len(args) < 2:
        return resp.arity_error("set")
    key, value = args[0], args[1]
    ex = None
    i = 2
    while i < len(args):
        opt = args[i].upper()
        if opt == "EX" and i + 1 < len(args):
            try:
                ex = int(args[i + 1])
                if ex <= 0:
                    return resp.error("ERR invalid expire time in 'set' command")
            except ValueError:
                return resp.error("ERR value is not an integer or out of range")
            i += 2
        else:
            return resp.error("ERR syntax error")
    set_value(key, value, "string")
    if ex is not None:
        from app.datastore.repository import set_expiry
        set_expiry(key, ex)
    else:
        from app.datastore.repository import set_expiry
        set_expiry(key, None)
    return resp.simple_string("OK")


async def handle_get(args: list[str], session) -> bytes:
    if len(args) != 1:
        return resp.arity_error("get")
    value, type_ = get_value(args[0])
    if value is None:
        return resp.null_bulk()
    if type_ != "string":
        return resp.error("WRONGTYPE Operation against a key holding the wrong kind of value")
    return resp.bulk_string(value)


async def handle_incr(args: list[str], session) -> bytes:
    if len(args) != 1:
        return resp.arity_error("incr")
    try:
        return resp.integer(incr_value(args[0]))
    except ValueError as e:
        return resp.error(str(e))


async def handle_decr(args: list[str], session) -> bytes:
    if len(args) != 1:
        return resp.arity_error("decr")
    try:
        return resp.integer(incr_value(args[0], by=-1))
    except ValueError as e:
        return resp.error(str(e))


async def handle_incrby(args: list[str], session) -> bytes:
    if len(args) != 2:
        return resp.arity_error("incrby")
    try:
        by = int(args[1])
    except ValueError:
        return resp.error("ERR value is not an integer or out of range")
    try:
        return resp.integer(incr_value(args[0], by=by))
    except ValueError as e:
        return resp.error(str(e))


async def handle_decrby(args: list[str], session) -> bytes:
    if len(args) != 2:
        return resp.arity_error("decrby")
    try:
        by = int(args[1])
    except ValueError:
        return resp.error("ERR value is not an integer or out of range")
    try:
        return resp.integer(incr_value(args[0], by=-by))
    except ValueError as e:
        return resp.error(str(e))
