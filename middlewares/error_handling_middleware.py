from typing import Callable, Any
import logging

from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware


class ErrorHandlingMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable, event: types.Update, data: dict[str, Any]
    ) -> Any:
        """Middleware to handle errors globally."""
        try:
            return await handler(event, data)
        except Exception as exception:
            if isinstance(event, types.Update) and event.message:
                await event.message.reply(f"Error: {str(exception)}")
            logging.error(f"Unhandled exception: {exception}", exc_info=True)
            return None
