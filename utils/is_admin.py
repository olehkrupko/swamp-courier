from aiogram.types import Chat

from os import getenv


def is_admin(chat: Chat) -> bool:
    """
    Check chat is considered to be with admin.

    Args:
        chat: The chat object to check.

    Returns:
        bool: True if the user is an admin, False otherwise.
    """
    return chat.id == int(getenv("TELEGRAM_CHATID"))
