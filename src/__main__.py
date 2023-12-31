from datetime import datetime
from typing import Annotated

import env
import uvicorn
from fastapi import FastAPI, Header
from lib import OK, error, makeResult
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
    no_sound: bool = False
    schedule_date: int | None = None


@app.post("/copyMessages")
async def _(opts: CopyMessageOptions, token: TokenHeader):
    if token != TOKEN:
        return error("Bad token")
    schedule_date: datetime | None = None
    try:
        if opts.schedule_date:
            schedule_date = datetime.fromtimestamp(opts.schedule_date)
        message_ids = await userbot.copy_messages(
            opts.chat_id,
            opts.from_chat_id,
            opts.message_ids,
            opts.as_forward,
            schedule_date,
            opts.no_sound,
        )
    except (ValueError, RPCError) as e:
        return error(e)
    return makeResult({"message_ids": message_ids})


class GetPostMessagesOptions(BaseModel):
    chat_id: int | str
    message_id: int


@app.post("/getPostMessages")
async def _(opts: GetPostMessagesOptions, token: TokenHeader):
    if token != TOKEN:
        return error("Bad token")
    try:
        r = await userbot.get_post_messages(opts.chat_id, opts.message_id)
    except (ValueError, RPCError) as e:
        return error(e)
    return makeResult(r)


class ReschedulePostOptions(BaseModel):
    chat_id: int | str
    message_ids: list[int]
    date: float


class DeletePostOptions(BaseModel):
    chat_id: int | str
    message_ids: list[int]


@app.post("/reschedulePost")
async def _(opts: ReschedulePostOptions, token: TokenHeader):
    if token != TOKEN:
        return error("Bad token")
    try:
        await userbot.reschedule_post(opts.chat_id, opts.message_ids, opts.date)
    except (ValueError, RPCError) as e:
        return error(e)
    return OK


@app.post("/deletePost")
async def _(opts: DeletePostOptions, token: TokenHeader):
    if token != TOKEN:
        return error("Bad token")
    try:
        await userbot.delete_post(opts.chat_id, opts.message_ids)
    except (ValueError, RPCError) as e:
        return error(e)
    return OK


uvicorn.run(app, port=env.get_int("PORT"))  # type: ignore
