import env
from telethon import TelegramClient
from telethon.functions import messages

API_ID = env.get_int("API_ID")
API_HASH = env.get("API_HASH")


client = TelegramClient(
    "session2",
    API_ID,
    API_HASH,
    device_model="CPython 3.10.5",
    system_version="Windows 10",
    app_version="Pyrogram 2.0.106",
    system_lang_code="en",
    lang_code="en",
)


async def main():
    # msg = await client.send_message("me", "123", schedule=time() + 100000)
    chat = await client.get_input_entity("me")
    # result = await client(messages.GetScheduledHistoryRequest(peer=chat, hash=0))
    # print(result)
    res = await client(messages.DeleteScheduledMessagesRequest(chat, [3, 4]))
    print(res)


with client:
    client.loop.run_until_complete(main())
