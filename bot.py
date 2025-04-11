import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import handlers  # import handlers to register them
from config.dispatcher import dp
from middlewares.error_handling_middleware import ErrorHandlingMiddleware


# Add the error-handling middleware
dp.update.outer_middleware(ErrorHandlingMiddleware())


async def main() -> None:
    bot = Bot(
        token=getenv("TELEGRAM_BOTTOKEN"),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True,
        ),
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
