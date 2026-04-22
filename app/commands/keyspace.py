from __future__ import annotations

from app.client import resp
from app.datastore import del_value, exists, type_of, keys_matching, get_ttl


async def handle_del(args: list[str], session) -> bytes:
    if not args:
        return resp.error("ERR wrong number of arguments for 'del' command")
    deleted = 0
    for key in args:
        deleted += int(del_value(key))
    return resp.integer(deleted)


async def handle_exists(args: list[str], session) -> bytes:
    if not args:
        return resp.error("ERR wrong number of arguments for 'exists' command")
    return resp.integer(sum(1 for key in args if exists(key)))


async def handle_type(args: list[str], session) -> bytes:
    if len(args) != 1:
        return resp.error("ERR wrong number of arguments for 'type' command")
    return resp.bulk_string(type_of(args[0]))


async def handle_keys(args: list[str], session) -> bytes:
    if len(args) != 1:
        return resp.arity_error("keys")
    return resp.array(keys_matching(args[0]))


async def handle_ttl(args: list[str], session) -> bytes:
    if len(args) != 1:
        return resp.arity_error("ttl")
    return resp.integer(get_ttl(args[0]))
