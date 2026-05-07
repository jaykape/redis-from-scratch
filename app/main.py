from __future__ import annotations

import asyncio
import sys
from pathlib import Path

from app.client.handler import handle_client
from app.config import CONFIG, load_config_file, set_startup_config


DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "redis.conf"


def _parse_args() -> None:
    """Config options via args at startup command"""
    if DEFAULT_CONFIG_PATH.is_file():
        try:
            load_config_file(str(DEFAULT_CONFIG_PATH))
        except (OSError, ValueError, KeyError) as exc:
            print(
                f"Warning: failed to load default config file '{DEFAULT_CONFIG_PATH}': {exc}",
                file=sys.stderr,
            )

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        current = args[i]
        if current == "--config":
            if i + 1 >= len(args):
                print("Warning: '--config' requires a value, ignoring.",
                      file=sys.stderr)
                i += 1
                continue
            try:
                load_config_file(args[i + 1])
            except (OSError, ValueError, KeyError) as exc:
                print(
                    f"Warning: failed to load config file '{args[i + 1]}': {exc}", file=sys.stderr)
            i += 2
            continue

        if not current.startswith("--"):
            try:
                load_config_file(current)
            except (OSError, ValueError, KeyError) as exc:
                print(
                    f"Warning: failed to load config file '{current}': {exc}", file=sys.stderr)
            i += 1
            continue

        key = args[i].lstrip("-").lower()
        if i + 1 >= len(args) or args[i + 1].startswith("--"):
            print(
                f"Warning: '{key}' requires a value, ignoring.", file=sys.stderr)
            i += 1
            continue
        value = args[i + 1]
        i += 2
        try:
            set_startup_config(key, value)
        except KeyError:
            print(
                f"Warning: unknown config key '{key}', ignoring.", file=sys.stderr)
        except ValueError as e:
            print(
                f"Warning: invalid value for '{key}': {e}, ignoring.", file=sys.stderr)


async def _shutdown_server(server: asyncio.Server) -> None:
    print("Shutting down server . . .")
    server.close()
    await server.wait_closed()
    print("Server stopped.")


async def main() -> None:
    """Server entry point"""
    _parse_args()
    host = CONFIG["bind"].value
    port = int(CONFIG["port"].value)
    server = await asyncio.start_server(handle_client, host, port)
    print(
        f"Redis server by jaykape started on {host}:{port}  \nPress Ctrl+C to stop.")
    try:
        async with server:
            await server.serve_forever()
    finally:
        await _shutdown_server(server)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
