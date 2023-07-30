import env
from lib import run
from pyrogram.client import Client

API_ID = env.get("API_ID")
API_HASH = env.get("API_HASH")


async def main():
    async with Client("userbot", API_ID, API_HASH, in_memory=True) as client:
        result = await client.export_session_string()
        print(result)


run(main())
