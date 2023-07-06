from datetime import datetime

import env
from client import Client


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
        await client.forward_messages(
            chat_id,
            from_chat_id,
            message_ids,
            drop_author=not as_forward,
            schedule_date=schedule_date,
            disable_notification=no_sound,
        )


userbot = Userbot(env.get("SESSION_STRING"))
