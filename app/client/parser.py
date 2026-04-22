"""Parse bytes into command and arguments"""


def parse(buffer: bytes):
    if not buffer:
        return None

    if buffer[:1] == b'*':
        return parse_resp(buffer)
    return parse_inline(buffer)


def parse_resp(buffer: bytes):
    """
    Parse a RESP array of bulk strings.

    Expected format:
    *<num>\r\n
    $<len>\r\n<data>\r\n
    ...

    Return: ((cmd, args), bytes_used) or None
    """

    end = buffer.find(b'\r\n')
    if end == -1:
        return None

    try:
        num = int(buffer[1:end])
    except ValueError:
        raise ValueError("Invalid array length")

    idx = end + 2
    parts = []

    for i in range(num):
        if idx >= len(buffer):
            return None

        if buffer[idx:idx + 1] != b'$':
            raise ValueError("Expected bulk string")

        end = buffer.find(b'\r\n', idx)
        if end == -1:
            return None
        try:
            length = int(buffer[idx+1:end])
        except ValueError:
            return ValueError("Invalid bulk string length")

        idx = end + 2
        if idx + length + 2 > len(buffer):
            return None

        data = buffer[idx:idx + length]
        parts.append(data.decode())

        idx += length + 2

    if not parts:
        raise ValueError("Empty command")

    cmd = parts[0].upper()
    args = parts[1:]

    return (cmd, args), idx


def parse_inline(buffer: bytes):
    """
    Parse inline command such as PING
    """

    end = buffer.find(b'\r\n')
    if end == -1:
        return None

    line = buffer[:end].decode().strip()
    if not line:
        return None

    parts = line.split()
    cmd = parts[0]
    args = parts[1:]

    return (cmd, args), end + 2
