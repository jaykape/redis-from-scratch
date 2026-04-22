from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from app.client import resp
from app.security import authenticate_session

if TYPE_CHECKING:
    from app.client.session import ClientSession


async def handle_ping(args: list[str], session: "ClientSession") -> bytes:
    if len(args) > 1:
        return resp.arity_error("ping")
    if args:
        return resp.bulk_string(args[0])
    return resp.simple_string("PONG")


async def handle_echo(args: list[str], session: "ClientSession") -> bytes:
    if len(args) != 1:
        return resp.arity_error("echo")
    return resp.bulk_string(args[0])


def _client_id_as_int(session: "ClientSession") -> int:
    try:
        return uuid.UUID(session.client_id).int & ((1 << 63) - 1)
    except (ValueError, AttributeError):
        return abs(hash(session.client_id))


async def handle_hello(args: list[str], session: "ClientSession") -> bytes:
    proto = session.resp_version
    i = 0
    if i < len(args) and args[i].isdigit():
        proto = int(args[i])
        if proto not in {2, 3}:
            return resp.error("NOPROTO unsupported protocol version")
        i += 1

    while i < len(args):
        token = args[i].upper()
        if token == "SETNAME" and i + 1 < len(args):
            session.client_name = args[i + 1]
            i += 2
            continue
        if token == "AUTH" and i + 2 < len(args):
            try:
                authenticate_session(session, args[i + 1], args[i + 2])
            except ValueError as exc:
                return resp.error(str(exc))
            i += 3
            continue
        return resp.error("ERR syntax error")

    session.resp_version = proto
    return resp.array([
        "server", "redis",
        "version", "app3-simplified",
        "proto", proto,
        "id", _client_id_as_int(session),
        "mode", "standalone",
        "role", "master",
        "modules", [],
    ])


async def handle_client(args: list[str], session: "ClientSession") -> bytes:
    if not args:
        return resp.arity_error("client")

    sub = args[0].upper()
    if sub == "ID" and len(args) == 1:
        return resp.integer(_client_id_as_int(session))
    if sub == "SETNAME" and len(args) == 2:
        session.client_name = args[1]
        return resp.simple_string("OK")
    if sub == "SETINFO" and len(args) == 3:
        field = args[1].upper()
        if field == "LIB-NAME":
            session.client_library_name = args[2]
        elif field == "LIB-VER":
            session.client_library_version = args[2]
        return resp.simple_string("OK")
    if sub == "GETNAME" and len(args) == 1:
        if session.client_name is None:
            return resp.null_bulk()
        return resp.bulk_string(session.client_name)

    return resp.error("ERR syntax error")
