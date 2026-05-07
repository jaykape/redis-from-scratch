from __future__ import annotations

from dataclasses import dataclass

from app.client import resp
from app.client.string import string_etc, string_get, string_numeric, string_set
from app.commands.connection import connection
from app.commands.server import server
from app.commands.generic import generic as keyspace


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


STRING_COMMANDS: dict[str, CommandSpec] = {
    "APPEND": CommandSpec(string_etc.handle_append, is_write=True),
    "SET": CommandSpec(string_set.handle_set, is_write=True),
    "GET": CommandSpec(string_get.handle_get),
    "INCR": CommandSpec(string_numeric.handle_incr, is_write=True),
    "DECR": CommandSpec(string_numeric.handle_decr, is_write=True),
    "INCRBY": CommandSpec(string_numeric.handle_incrby, is_write=True),
    "DECRBY": CommandSpec(string_numeric.handle_decrby, is_write=True),
    "INCRBYFLOAT": CommandSpec(string_numeric.handle_incrbyfloat, is_write=True),
}

HASH_COMMANDS: dict[str, CommandSpec] = {

}

LIST_COMMANDS: dict[str, CommandSpec] = {

}

SET_COMMANDS: dict[str, CommandSpec] = {

}

SORTED_SET_COMMANDS: dict[str, CommandSpec] = {

}

STREAM_COMMANDS: dict[str, CommandSpec] = {

}

BITMAP_COMMANDS: dict[str, CommandSpec] = {

}

HYPERLOGLOG_COMMANDS: dict[str, CommandSpec] = {

}

GEOSPATIAL_COMMANDS: dict[str, CommandSpec] = {

}

JSON_COMMANDS: dict[str, CommandSpec] = {

}

SEARCH_COMMANDS: dict[str, CommandSpec] = {

}

TIME_SERIES_COMMANDS: dict[str, CommandSpec] = {

}

VECTOR_SET_COMMANDS: dict[str, CommandSpec] = {

}

PUB_SUB_COMMANDS: dict[str, CommandSpec] = {

}

TRANSACTION_COMMANDS: dict[str, CommandSpec] = {

}


SCRIPTING_COMMANDS: dict[str, CommandSpec] = {

}

CONNECTION_COMMANDS: dict[str, CommandSpec] = {
    "AUTH": CommandSpec(connection.handle_auth, bypass_auth=True),
    "PING": CommandSpec(connection.handle_ping, bypass_auth=True),
    "ECHO": CommandSpec(connection.handle_echo),
    "HELLO": CommandSpec(connection.handle_hello, bypass_auth=True),
    "CLIENT": CommandSpec(connection.handle_client),
    "QUIT": CommandSpec(_quit_command, bypass_auth=True),
    "SELECT": CommandSpec(server.handle_select),
}

SERVER_COMMANDS: dict[str, CommandSpec] = {
    "ACL": CommandSpec(server.handle_acl),
    "CONFIG": CommandSpec(server.handle_config),
}

CLUSTER_COMMANDS: dict[str, CommandSpec] = {
}

GENERIC_COMMANDS: dict[str, CommandSpec] = {
    "DEL": CommandSpec(keyspace.handle_del, is_write=True),
    "EXISTS": CommandSpec(keyspace.handle_exists),
    "TYPE": CommandSpec(keyspace.handle_type),
    "KEYS": CommandSpec(keyspace.handle_keys),
    "TTL": CommandSpec(keyspace.handle_ttl),
}

COMMANDS = build_command_table(
    CONNECTION_COMMANDS,
    STRING_COMMANDS,
    GENERIC_COMMANDS,
    SERVER_COMMANDS,
)
