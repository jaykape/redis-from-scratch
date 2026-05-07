
from app.client import resp
from app.datastore.repository import get_value, set_value


async def handle_append(args, session):
    if len(args) != 2:
        return resp.arity_error("append")
    key, append_value = args[0], args[1]
    value, type_ = get_value(key)
    if value is not None and type_ != "string":
        return resp.wrongtype_error()
    if value is None:
        set_value(key, append_value, "string")
        return resp.integer(len(append_value))
    else:
        set_value(key, value + append_value, "string")
        return resp.integer(len(value) + len(append_value))


async def handle_setrange(args, session):
    pass


async def handle_getset(args, session):
    pass


async def handle_getdel(args, session):
    pass


async def handle_getex(args, session):
    pass


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
