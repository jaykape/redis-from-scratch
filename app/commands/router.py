from app.commands.registry import COMMANDS
from app.client import resp
from app.security import check_command_permission
from app.state import CURRENT_DB


async def execute_command(
        cmd: str,
        args: list[str],
        session: "ClientSession") -> bytes:

    upper = cmd.upper()
    try:
        spec = COMMANDS.get(upper)
        if spec is None:
            return resp.error(f"ERR unknown command '{cmd.lower()}'")

        if not spec.bypass_auth:
            if not session.authenticated:
                return resp.error("NOAUTH Authentication required.")
            acl_error = check_command_permission(session, upper)
            if acl_error is not None:
                return resp.error(acl_error)

        token = CURRENT_DB.set(session.db)
        try:
            response = await spec.runner(args, session)
        finally:
            CURRENT_DB.reset(token)

        return response

    except Exception:
        return resp.error("ERR internal server error")
