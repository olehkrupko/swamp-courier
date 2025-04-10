from os import getenv

from aiogram.types import Message

from config.dispatcher import dp
from services.swamp_api_service import SwampApiService


@dp.message()
async def admin_default_handler(message: Message) -> None:
    """Handler that only works for a specific chat ID."""
    telegram_admin_chatid = getenv("TELEGRAM_ADMIN_CHATID")

    if not telegram_admin_chatid:
        raise ValueError("TELEGRAM_ADMIN_CHATID environment variable is not set.")
    if message.chat.id != telegram_admin_chatid:
        raise PermissionError("Access denied.")

    # Use the service function to send the API request
    response = await SwampApiService.explain_feed_href(message.text)

    await message.reply(f"API Response: {response}")
