from __future__ import annotations

import asyncio
from app.client.parser import parse
from app.client.session import ClientSession
from app.commands import execute_command


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    """Handle accepted connections"""

    session = ClientSession()
    buffer = b""

    try:
        while True:
            chunk = await reader.read(4096)
            if not chunk:
                break

            buffer += chunk

            while True:
                result = parse(buffer)
                if result is None:
                    break

                (cmd, args), used = result
                buffer = buffer[used:]

                response = await execute_command(cmd, args, session)
                if response:
                    writer.write(response)

            await writer.drain()

    finally:
        writer.close()
        await writer.wait_closed()
