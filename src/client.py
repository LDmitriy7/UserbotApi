from datetime import datetime
from typing import Any, Iterable, cast

import pyrogram
from pyrogram.raw.functions.messages.delete_scheduled_messages import (
    DeleteScheduledMessages,
)
from pyrogram.raw.functions.messages.edit_message import EditMessage
from pyrogram.raw.functions.messages.forward_messages import ForwardMessages
from pyrogram.raw.types import (
    UpdateNewChannelMessage,
    UpdateNewMessage,
    UpdateNewScheduledMessage,
)
from pyrogram.types import Message
from pyrogram.types.list import List
from pyrogram.utils import datetime_to_timestamp


class Client(pyrogram.Client):
    def __init__(self, session_string: str):
        super().__init__("userbot", session_string=session_string)  # type: ignore

    async def invoke(self, *args, **kwargs):  # type: ignore
        return await super().invoke(*args, **kwargs)  # type: ignore

    async def edit_message(
        self,
        chat_id: int | str,
        message_id: int,
        text: str | None = None,
        schedule_date: int | None = None,
    ):
        await self.invoke(  # type: ignore
            EditMessage(
                peer=await self.resolve_peer(chat_id),  # type: ignore
                id=message_id,
                message=text,
                schedule_date=schedule_date,
            )
        )
        return True

    async def delete_scheduled_messages(
        self,
        chat_id: int | str,
        message_ids: list[int],
    ):
        r: Any = await self.invoke(  # type: ignore
            DeleteScheduledMessages(
                peer=await self.resolve_peer(chat_id),  # type: ignore
                id=message_ids,
            )
        )
        print(r)
        return True

    async def forward_messages(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_ids: int | Iterable[int],
        disable_notification: bool | None = None,
        schedule_date: datetime | None = None,
        protect_content: bool | None = None,
        drop_author: bool | None = None,
    ) -> Message | list[Message]:
        is_iterable = not isinstance(message_ids, int)
        message_ids = list(message_ids) if is_iterable else [message_ids]
        r: Any = await self.invoke(  # type: ignore
            ForwardMessages(
                to_peer=await self.resolve_peer(chat_id),  # type: ignore
                from_peer=await self.resolve_peer(from_chat_id),  # type: ignore
                id=message_ids,
                silent=disable_notification or None,
                random_id=[self.rnd_id() for _ in message_ids],
                schedule_date=datetime_to_timestamp(schedule_date),
                noforwards=protect_content,
                drop_author=drop_author,
            )
        )
        forwarded_messages: list[Message] = []
        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}
        _types = UpdateNewMessage, UpdateNewChannelMessage, UpdateNewScheduledMessage
        for i in r.updates:
            if isinstance(i, _types):
                m = await Message._parse(self, i.message, users, chats)  # type: ignore
                forwarded_messages.append(cast(Message, m))
        return List(forwarded_messages) if is_iterable else forwarded_messages[0]
