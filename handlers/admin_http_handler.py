from hashlib import sha256
from os import getenv

from aiogram import F, Router as AiogramRouter
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from services.redis_service import RedisService
from services.swamp_api_service import SwampApiService
from utils.is_admin import is_admin


router = AiogramRouter(name=__name__)


@router.message(F.chat.func(is_admin) and F.text.contains("http"))
async def admin_http_handler(message: Message) -> None:
    """Handler that only works for links sent to a specific chat ID."""
    if not getenv("TELEGRAM_CHATID"):
        raise ValueError("TELEGRAM_CHATID environment variable is not set.")

    href = message.text

    # Use the service function to send the API request
    if getenv("TELEGRAM_AUTOCONFIRM"):
        feed = await SwampApiService.explain_feed_href(href, mode="push")
    else:
        feed = await SwampApiService.explain_feed_href(href)

    reply = ""
    if feed["similar_feeds"]:
        reply += "<b>[SIMILAR FEED(S) PRESENT, CANT SAVE]</b>\n\n"

    reply += "<b>EXPLAINED</b>:\n"
    reply += f"- {feed['explained']['title']}\n"
    reply += f"- {feed['explained']['href']}\n"
    reply += f"- {feed['explained']['frequency']}\n"
    reply += f"- {feed['explained']['json']}\n\n"

    reply += f"similar_feeds: {len(feed['similar_feeds'])}\n"
    for each in feed["similar_feeds"]:
        reply += f"<b>{each['_id']}</b>: {each['title']}\n"
        reply += f"    - created: {each['_created']}\n"
        if each["title"] != feed["explained"]["title"]:
            reply += f"    - title: {each['title']}\n"
        if each["frequency"] != feed["explained"]["frequency"]:
            reply += f"\t- frequency: {each['frequency']}"
        reply += "\n"

    if feed["similar_feeds"]:
        reply += "<b>[SIMILAR FEED(S) PRESENT, CANT SAVE]</b>"

    # Generate a unique identifier for the response
    href_id = sha256(href.encode()).hexdigest()[:16]

    # Store the response in Redis with a 1-hour expiration
    await RedisService.set_with_expiry(f"swamp-courier-explain:{href_id}", href, 3600)

    # Create an inline keyboard with a callback button
    inline_keyboard = [[]]
    if not feed["similar_feeds"] and not getenv("TELEGRAM_AUTOCONFIRM", False):
        inline_keyboard = [
            [InlineKeyboardButton(text="Save", callback_data=f"admin-save:{href_id}")]
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await message.reply(
        reply,
        reply_markup=keyboard,  # Ensure the keyboard is passed here
    )
