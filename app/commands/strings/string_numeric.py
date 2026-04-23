import math

from app.client import resp
from app.datastore.repository import get_value, set_value


async def handle_incr(args, session):
    if len(args) != 1:
        return resp.arity_error("incr")

    key = args[0]
    value, type_ = get_value(key)

    if value is not None and type_ != "string":
        return resp.wrongtype_error()

    if value is None:
        set_value(key, "1", "string")
        return resp.integer(1)

    try:
        num = int(value)
    except ValueError:
        return resp.error("ERR value is not an integer or out of range")

    num += 1
    set_value(key, str(num), "string")

    return resp.integer(num)


async def handle_incrby(args, session):
    if len(args) != 2:
        return resp.arity_error("incrby")

    key = args[0]

    try:
        by = int(args[1])
    except ValueError:
        return resp.error("ERR value is not an integer or out of range")

    value, type_ = get_value(key)

    if value is not None and type_ != "string":
        return resp.wrongtype_error()

    if value is None:
        set_value(key, str(by), "string")
        return resp.integer(by)

    try:
        num = int(value)
    except ValueError:
        return resp.error("ERR value is not an integer or out of range")

    num += by
    set_value(key, str(num), "string")

    return resp.integer(num)


async def handle_decr(args, session):
    if len(args) != 1:
        return resp.arity_error("decr")
    key = args[0]
    value, type_ = get_value(key)
    if value is not None and type_ != "string":
        return resp.wrongtype_error()
    if value is None:
        set_value(key, "-1", "string")
        return resp.integer(-1)
    try:
        num = int(value)
    except ValueError:
        return resp.error("ERR value is not an integer or out of range")
    num -= 1
    set_value(key, str(num), "string")
    return resp.integer(num)


async def handle_decrby(args, session):
    if len(args) != 2:
        return resp.arity_error("decrby")

    key = args[0]

    try:
        by = int(args[1])
    except ValueError:
        return resp.error("ERR value is not an integer or out of range")

    value, type_ = get_value(key)

    if value is not None and type_ != "string":
        return resp.wrongtype_error()

    if value is None:
        set_value(key, str(-by), "string")
        return resp.integer(-by)

    try:
        num = int(value)
    except ValueError:
        return resp.error("ERR value is not an integer or out of range")

    num -= by
    set_value(key, str(num), "string")

    return resp.integer(num)


async def handle_incrbyfloat(args, session):
    if len(args) != 2:
        return resp.arity_error("incrbyfloat")

    key = args[0]

    try:
        by = float(args[1])
    except ValueError:
        return resp.error("ERR value is not a float or out of range")

    value, type_ = get_value(key)

    if value is not None and type_ != "string":
        return resp.wrongtype_error()

    try:
        if value is None:
            num = by
        else:
            num = float(value) + by

        if math.isnan(num) or math.isinf(num):
            return resp.error("ERR value is not float or out of range")

        s = format(num, ".17f")
        s = s.rstrip("0").rstrip(".")
        if s == "-0":
            s = "0"

        set_value(key, s, "string")
        return resp.bulk_string(s)

    except ValueError:
        return resp.error("ERR value is not a float or out of range")

    set_value(key, s, "string")

    return resp.bulk_string(s)
