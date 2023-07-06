import asyncio
from typing import Any, Awaitable


def resp(ok: bool, error: str | None = None):
    return {"ok": ok, "error": error}


def error(e: Exception | str):
    return resp(False, str(e))


OK = resp(True)


def run(coro: Awaitable[Any]):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(coro)
