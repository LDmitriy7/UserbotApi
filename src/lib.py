import asyncio
from typing import Any, Awaitable

Result = dict[Any, Any] | list[Any] | None


def resp(ok: bool, error: str | None = None, result: Result = None):
    return {"ok": ok, "error": error, "result": result}


def error(e: Exception | str):
    return resp(False, str(e))


OK = resp(True)


def makeResult(result: Result):
    return resp(True, result=result)


def run(coro: Awaitable[Any]):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(coro)
