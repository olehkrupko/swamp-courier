import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.dispatcher import dp

import handlers  # import handlers to register them


async def main() -> None:
    bot = Bot(
        token=getenv("TELEGRAM_BOTTOKEN"),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
