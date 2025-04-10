from os import getenv

from aiogram.types import Message

from config.dispatcher import dp


@dp.message()
async def admin_default_handler(message: Message) -> None:
    """Handler that only works for a specific chat ID."""
    if getenv("SPECIFIC_CHAT_ID") and message.chat.id == getenv("SPECIFIC_CHAT_ID"):
        await message.reply("You have access to this handler!")
    else:
        await message.reply("Access denied.")
