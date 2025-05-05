import asyncio
import logging
import sys
from datetime import datetime
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
    # set up and log the bot in
    bot = Bot(
        token=getenv("TELEGRAM_BOTTOKEN"),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True,
        ),
    )

    # Send message to admin on startup
    await bot.send_message(
        chat_id=getenv("TELEGRAM_CHATID"),
        text="{dt} - Bot started successfully!".format(
            dt=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    # Start polling received messages
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
