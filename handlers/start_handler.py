from aiogram import html
from aiogram.filters import CommandStart
from aiogram.types import Message

from config.dispatcher import dp


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """This handler receives messages with `/start` command."""
    reply = (
        f"Hello, {html.bold(message.from_user.full_name)}!\n"
        "\n"
        "I am a bot that helps you to save feeds to swamp-api.\n"
        "Feel free to check out my code at https://github.com/olehkrupko/swamp-courier\n"
        "\n"
        f"Your Chat ID: { html.bold(message.chat.id) }"
    )

    await message.reply(reply)
