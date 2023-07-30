from time import time

from lib import run
from userbot import userbot


async def main():
    result = await userbot.reschedule_post(-1001585027208, [177, 178], time() + 500)
    print(result)


run(main())
