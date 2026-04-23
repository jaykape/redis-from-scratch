
from app.client import resp
from app.datastore.repository import set_value


async def handle_set(args, session):
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


async def handle_set(args, session):
    # ...existing code or import from old handler...
    pass


async def handle_setex(args, session):
    pass


async def handle_setnx(args, session):
    pass


async def handle_mset(args, session):
    pass


async def handle_msetnx(args, session):
    pass


async def handle_msetex(args, session):
    pass
