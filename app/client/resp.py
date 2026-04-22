from __future__ import annotations


def simple_string(value: str) -> bytes:
    return f"+{value}\r\n".encode()


def error(message: str) -> bytes:
    return f"-{message}\r\n".encode()


def arity_error(command: str) -> bytes:
    return error(f"ERR wrong number of arguments for '{command}' command")


def integer(value: int) -> bytes:
    return f":{value}\r\n".encode()


def bulk_string(value: str) -> bytes:
    data = str(value).encode()
    return f"${len(data)}\r\n".encode() + data + b"\r\n"


def null_bulk() -> bytes:
    return b"$-1\r\n"


def array(items: list[object]) -> bytes:
    result = [f"*{len(items)}\r\n".encode()]
    for item in items:
        result.append(_encode_item(item))
    return b"".join(result)


def is_error(value: bytes) -> bool:
    return value.startswith(b"-")


def _encode_item(value: object) -> bytes:
    if value is None:
        return null_bulk()
    if isinstance(value, bytes):
        return value
    if isinstance(value, int):
        return integer(value)
    if isinstance(value, str):
        return bulk_string(value)
    if isinstance(value, list):
        return array(value)
    raise TypeError(f"Unsupported RESP item: {type(value)!r}")
