from aiogram import html
from aiogram.filters import CommandStart
from aiogram.types import Message

from config.dispatcher import dp


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """This handler receives messages with `/start` command."""
    await message.reply(f"Hello, {html.bold(message.from_user.full_name)}!")
