
from app.client import resp
from app.datastore.repository import get_value


async def handle_get(args, session):
    if len(args) != 1:
        return resp.arity_error("get")
    value, type_ = get_value(args[0])
    if value is None:
        return resp.null_bulk()
    if type_ != "string":
        return resp.wrongtype_error()
    return resp.bulk_string(value)


async def handle_getrange(args, session):
    pass


async def handle_getdel(args, session):
    pass


async def handle_getex(args, session):
    pass


async def handle_strlen(args, session):
    pass


async def handle_substr(args, session):
    pass


async def handle_get(args, session):
    # ...existing code or import from old handler...
    pass


async def handle_mget(args, session):
    pass


async def handle_strlen(args, session):
    pass


async def handle_getrange(args, session):
    pass


async def handle_substr(args, session):
    pass
