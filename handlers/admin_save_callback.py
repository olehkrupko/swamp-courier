from aiogram.types import CallbackQuery
from aiogram import F, Router as AiogramRouter

from services.redis_service import RedisService
from services.swamp_api_service import SwampApiService
from utils.is_admin import is_admin


router = AiogramRouter(name=__name__)


# requires TELEGRAM_AUTOCONFIRM=false to function
# if it's true, feed will be authomatically saved
# and the button won't be shown
@router.callback_query(
    lambda c: F.chat.func(is_admin) and c.data and c.data.startswith("admin-save:")
)
async def admin_save_callback(callback_query: CallbackQuery) -> None:
    """Process Save button callback for admin_http_handler."""
    href_id = callback_query.data.split("admin-save:")[1]

    # Retrieve the response from Redis
    href = await RedisService.get(f"swamp-courier-explain:{href_id}")

    if not href:
        await callback_query.message.answer("Error: Response not found or expired.")
        await callback_query.answer()  # Acknowledge the callback
        return

    # Process the response (e.g., save it to a database or perform another action)
    feed = await SwampApiService.explain_feed_href(href, mode="push")
    reply = "<b>SAVED</b>:\n"
    reply += f"- {feed['explained']['_id']}\n"
    reply += f"- {feed['explained']['title']}\n"
    reply += f"- {feed['explained']['href']}\n"
    reply += f"- {feed['explained']['frequency']}\n"
    reply += f"- {feed['explained']['json']}\n\n"

    print(f"Response to admin-save: {href}")
    await callback_query.message.answer(reply)
    await callback_query.answer()  # Acknowledge the callback
