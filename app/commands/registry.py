from __future__ import annotations

from dataclasses import dataclass

from app.client import resp
from app.commands import strings, auth, connection, keyspace, server


@dataclass(frozen=True)
class CommandSpec:
    runner: CommandRunner
    is_write: bool = False
    bypass_auth: bool = False


async def _quit_command(args: list[str], session: "ClientSession") -> bytes:
    return resp.simple_string("OK")


def build_command_table(*groups: dict[str, CommandSpec]) -> dict[str, CommandSpec]:
    commands: dict[str, CommandSpec] = {}
    for group in groups:
        duplicates = commands.keys() & group.keys()
        if duplicates:
            joined = ", ".join(sorted(duplicates))
            raise ValueError(f"Duplicate command registrations: {joined}")
        commands.update(group)
    return commands


CONNECTION_COMMANDS: dict[str, CommandSpec] = {
    "PING": CommandSpec(connection.handle_ping, bypass_auth=True),
    "ECHO": CommandSpec(connection.handle_echo),
    "HELLO": CommandSpec(connection.handle_hello, bypass_auth=True),
    "CLIENT": CommandSpec(connection.handle_client),
    "QUIT": CommandSpec(_quit_command, bypass_auth=True),
}

AUTH_COMMANDS: dict[str, CommandSpec] = {
    "AUTH": CommandSpec(auth.handle_auth, bypass_auth=True),
    "ACL": CommandSpec(auth.handle_acl),
}

STRING_COMMANDS: dict[str, CommandSpec] = {
    "APPEND": CommandSpec(strings.handle_append, is_write=True),
    "SET": CommandSpec(strings.handle_set, is_write=True),
    "GET": CommandSpec(strings.handle_get),
    "INCR": CommandSpec(strings.handle_incr, is_write=True),
    "DECR": CommandSpec(strings.handle_decr, is_write=True),
    "INCRBY": CommandSpec(strings.handle_incrby, is_write=True),
    "DECRBY": CommandSpec(strings.handle_decrby, is_write=True),
}

KEYSPACE_COMMANDS: dict[str, CommandSpec] = {
    "DEL": CommandSpec(keyspace.handle_del, is_write=True),
    "EXISTS": CommandSpec(keyspace.handle_exists),
    "TYPE": CommandSpec(keyspace.handle_type),
    "KEYS": CommandSpec(keyspace.handle_keys),
    "TTL": CommandSpec(keyspace.handle_ttl),
}

SERVER_COMMANDS: dict[str, CommandSpec] = {
    "SELECT": CommandSpec(server.handle_select),
    "CONFIG": CommandSpec(server.handle_config),
}

COMMANDS = build_command_table(
    CONNECTION_COMMANDS,
    AUTH_COMMANDS,
    STRING_COMMANDS,
    KEYSPACE_COMMANDS,
    SERVER_COMMANDS,
)
