from aiogram.types import Message

from config.dispatcher import dp


@dp.message()
async def echo_handler(message: Message) -> None:
    """Handler will reply to the received message."""
    try:
        await message.reply(message.text)
    except TypeError:
        await message.answer("Nice try!")
