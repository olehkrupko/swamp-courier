from aiogram.types import Message
from config.dispatcher import dp

@dp.message()
async def echo_handler(message: Message) -> None:
    """Handler will forward received messages back to the sender."""
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")
