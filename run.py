import asyncio
import logging
import sys
from datetime import datetime
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import handlers
from middlewares.error_handling_middleware import ErrorHandlingMiddleware


async def main() -> None:
    # set up and log the bot in
    bot = Bot(
        token=getenv("TELEGRAM_BOTTOKEN"),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True,
        ),
    )

    disp = Dispatcher(bot=bot)

    print(f"{type(handlers.command_start_handler.router)=} {handlers.command_start_handler.router=}")
    print(f"{type(handlers.command_start_handler.test)=} {handlers.command_start_handler.test=}")
    print(f"{type(handlers.admin_http_handler.router)=} {handlers.admin_http_handler.router=}")
    print(f"{type(handlers.admin_save_callback.router)=} {handlers.admin_save_callback.router=}")
    # Register start handler
    disp.include_routers(
        [
            handlers.command_start_handler.router,
            handlers.admin_http_handler.router,
            handlers.admin_save_callback.router,
        ]
    )

    # Add the error-handling middleware
    disp.update.outer_middleware(ErrorHandlingMiddleware())

    # Send message to admin just before starting the bot
    await bot.send_message(
        chat_id=getenv("TELEGRAM_CHATID"),
        text="{dt} - Bot started successfully!".format(
            dt=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    # Start polling received messages
    await disp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
