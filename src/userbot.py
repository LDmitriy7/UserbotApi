from datetime import datetime

import env
from client import Client
from pyrogram.types import Message


class Userbot:
    def __init__(self, session_string: str) -> None:
        self.session_string = session_string
        self._client = Client(self.session_string)
        self._started = False

    async def get_client(self):
        if not self._started:
            await self._client.start()
            self._started = True
        return self._client

    async def get_post_messages(self, chat_id: int | str, message_id: int):
        client = await self.get_client()
        msgs = await client.get_media_group(chat_id, message_id)
        return [m.id for m in msgs]

    async def copy_messages(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_ids: list[int],
        as_forward: bool = False,
        schedule_date: datetime | None = None,
        no_sound: bool = False,
    ):
        client = await self.get_client()
        result = await client.forward_messages(
            chat_id,
            from_chat_id,
            message_ids,
            drop_author=not as_forward,
            schedule_date=schedule_date,
            disable_notification=no_sound,
        )
        if isinstance(result, Message):
            result = [result]
        return [i.id for i in result]

    async def reschedule_post(
        self,
        chat_id: int | str,
        message_ids: list[int],
        date: float,
    ):
        client = await self.get_client()
        return await client.edit_message(
            chat_id, message_ids[0], schedule_date=int(date)
        )

    async def delete_post(
        self,
        chat_id: int | str,
        message_ids: list[int],
    ):
        client = await self.get_client()
        return await client.delete_messages(chat_id, message_ids)


userbot = Userbot(env.get("SESSION_STRING"))
