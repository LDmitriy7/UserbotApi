from datetime import datetime
from typing import Annotated

import env
import uvicorn
from fastapi import FastAPI, Header
from lib import OK, error
from pydantic import BaseModel
from pyrogram.errors import RPCError
from userbot import userbot

TokenHeader = Annotated[str, Header()]
TOKEN = env.get("TOKEN")
app = FastAPI()


class CopyMessageOptions(BaseModel):
    chat_id: int | str
    from_chat_id: int | str
    message_ids: list[int]
    as_forward: bool = False
    schedule_date: int | None = None


@app.post("/copyMessages")
async def _(opts: CopyMessageOptions, token: TokenHeader):
    if token != TOKEN:
        return error("Bad token")
    schedule_date: datetime | None = None
    try:
        if opts.schedule_date:
            schedule_date = datetime.fromtimestamp(opts.schedule_date)
        await userbot.copy_messages(
            opts.chat_id,
            opts.from_chat_id,
            opts.message_ids,
            opts.as_forward,
            schedule_date,
        )
    except (ValueError, RPCError) as e:
        return error(e)
    return OK


uvicorn.run(app, port=env.get_int("PORT"))  # type: ignore
