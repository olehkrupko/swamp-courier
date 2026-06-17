import asyncio
import logging
import sys
from datetime import datetime
from os import getenv

import sentry_sdk
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import handlers
from middlewares.error_handling_middleware import ErrorHandlingMiddleware


sentry_sdk.init(
    dsn=getenv("SENTRY_SDK_DSN"),
    # Add data like request headers and IP for users, if applicable;
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # # Set traces_sample_rate to 1.0 to capture 100%
    # # of transactions for tracing.
    # traces_sample_rate=1.0,
    # # To collect profiles for all profile sessions,
    # # set `profile_session_sample_rate` to 1.0.
    # profile_session_sample_rate=1.0,
    # # Profiles will be automatically collected while
    # # there is an active span.
    # profile_lifecycle="trace",
    # # Enable logs to be sent to Sentry
    # enable_logs=True,
)


async def main() -> None:
    # Delay to allow other services to start
    await asyncio.sleep(5 * 60)

    # set up and log the bot in
    bot = Bot(
        token=getenv("TELEGRAM_BOTTOKEN"),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            link_preview_is_disabled=True,
        ),
    )

    disp = Dispatcher(bot=bot)

    # Register start handler
    disp.include_router(handlers.command_start_handler.router)
    # Register admin handlers
    disp.include_router(handlers.admin_http_handler.router)
    disp.include_router(handlers.admin_save_callback.router)

    # Add the error-handling middleware
    disp.update.outer_middleware(ErrorHandlingMiddleware())

    # Send message to admin just before starting the bot
    await bot.send_message(
        chat_id=getenv("TELEGRAM_CHATID"),
        text="{dt} - Bot started successfully!".format(
            dt=datetime.now().strftime("%Y-%m-%d %H:%M"),
        ),
    )

    # Start polling received messages
    await disp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
