from __future__ import annotations

import asyncio
import sys

from app.client import handle_client
from app.config import CONFIG, set_startup_config


def _parse_args() -> None:
    """Config options via args at startup command"""
    args = sys.argv[1:]
    i = 0
    while i < len(args):
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


async def main() -> None:
    """Server entry point"""
    _parse_args()
    port = int(CONFIG["port"].value)
    server = await asyncio.start_server(handle_client, "0.0.0.0", port)
    async with server:
        print(
            f"kapeRedis server started on port {port}. Press Ctrl+C to stop.")
        try:
            await server.serve_forever()
        except asyncio.CancelledError:
            pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped.")
