from app.client import resp


async def handle_mget(args, session):
    if len(args) == 0:
        return resp.arity_error("mget")
    result = []
    for i in range(len(args)):
        value, type_ = get_value(args[i])
        if type_ != "string":
            value = None
        result.append(value)
    return resp.array(result)


async def handle_mset(args, session):
    if len(args) % 2 != 0 or len(args) == 0:
        return resp.arity_error("mset")

    for i in range(len(args)//2):
        set_value(args[2 * i], args[2 * i + 1], "string")
        return resp.integer(1)


async def handle_msetx(args, session):
    pass


async def handle_msetnx(args, session):
    if len(args) % 2 != 0 or len(args) == 0:
        return resp.arity_error("msetnx")

    for i in range(len(args)//2):
        value, type_ = get_value(args[2 * i])
        if value is not None:
            return resp.integer(0)

    for i in range(len(args)//2):
        set_value(args[2 * i], args[2 * i + 1], "string")
        return resp.integer(1)
