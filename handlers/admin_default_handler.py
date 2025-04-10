from hashlib import sha256
from os import getenv

from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from magic_filter import F

from config.dispatcher import dp
from services.redis_service import RedisService
from services.swamp_api_service import SwampApiService


@dp.message(F.chat.func(lambda chat: chat.id == getenv("TELEGRAM_ADMIN_CHATID")) and F.text.contains("http"))
async def admin_default_handler(message: Message) -> None:
    """Handler that only works for a specific chat ID."""
    if not getenv("TELEGRAM_ADMIN_CHATID"):
        raise ValueError("TELEGRAM_ADMIN_CHATID environment variable is not set.")

    href = message.text

    # Use the service function to send the API request
    feed = await SwampApiService.explain_feed_href(href)

    reply = ""
    if feed["similar_feeds"]:
        reply += f"<b>[SIMILAR FEED(S) PRESENT, CANT SAVE]</b>\n\n"

    reply += "<b>EXPLAINED</b>:\n"
    reply += f"- {feed['explained']['title']}\n"
    reply += f"- {feed['explained']['href']}\n"
    reply += f"- {feed['explained']['frequency']}\n"
    reply += f"- {feed['explained']['json']}\n\n"

    reply += f"similar_feeds: {len(feed['similar_feeds'])}\n"
    for each in feed["similar_feeds"]:
        reply += f"- <b>{each['_id']}</b>: {each['title']}\n"
        reply += f"    - created: {each['_created']}\n"
        if each["title"] != feed["explained"]["title"]:
            reply += f"    - title: {each['title']}\n"
        if each["frequency"] != feed["explained"]["frequency"]:
            reply += f"\t- frequency: {each['frequency']}"
        reply += "\n"

    if feed["similar_feeds"]:
        reply += f"<b>[SIMILAR FEED(S) PRESENT, CANT SAVE]</b>"

    # Generate a unique identifier for the response
    href_id = sha256(href.encode()).hexdigest()[:16]

    # Store the response in Redis with a 1-hour expiration
    await RedisService.set_with_expiry(f"swamp-courier-explain:{href_id}", href, 3600)

    # Create an inline keyboard with a callback button
    inline_keyboard = [[]]
    if not feed["similar_feeds"]:
        inline_keyboard = [
            [InlineKeyboardButton(text="Save", callback_data=f"save:{href_id}")]
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await message.reply(
        reply,
        reply_markup=keyboard,  # Ensure the keyboard is passed here
    )


@dp.callback_query(lambda c: c.data and c.data.startswith("save:"))
async def save_callback_handler(callback_query: CallbackQuery) -> None:
    """Process the save button callback."""
    href_id = callback_query.data.split("save:")[1]

    # Retrieve the response from Redis
    href = await RedisService.get(f"swamp-courier-explain:{href_id}")

    if not href:
        await callback_query.message.answer("Error: Response not found or expired.")
        await callback_query.answer()  # Acknowledge the callback
        return

    # Process the response (e.g., save it to a database or perform another action)
    feed = await SwampApiService.explain_feed_href(href, mode="push")
    reply = "<b>SAVED**:\n"
    reply += f"- {feed['explained']['_id']}\n"
    reply += f"- {feed['explained']['title']}\n"
    reply += f"- {feed['explained']['href']}\n"
    reply += f"- {feed['explained']['frequency']}\n"
    reply += f"- {feed['explained']['json']}\n\n"

    print(f"Response to save: {href}") 
    await callback_query.message.answer(reply)
    await callback_query.answer()  # Acknowledge the callback
