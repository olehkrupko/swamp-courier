from hashlib import sha256
from os import getenv

from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from config.dispatcher import dp
from services.redis_service import RedisService
from services.swamp_api_service import SwampApiService


@dp.message()
async def admin_default_handler(message: Message) -> None:
    """Handler that only works for a specific chat ID."""
    telegram_admin_chatid = getenv("TELEGRAM_ADMIN_CHATID")

    if not telegram_admin_chatid:
        raise ValueError("TELEGRAM_ADMIN_CHATID environment variable is not set.")
    if message.chat.id != int(telegram_admin_chatid):
        raise PermissionError("Access denied.")
    if "http" not in message.text:
        raise ValueError("URL required.")

    # Use the service function to send the API request
    response = await SwampApiService.explain_feed_href(message.text)

    # Generate a unique identifier for the response
    response_id = sha256(str(message.text).encode()).hexdigest()[:16]

    # Store the response in Redis with a 1-hour expiration
    await RedisService.set_with_expiry(f"response:{response_id}", str(response), 3600)

    # Create an inline keyboard with a callback button
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Save", callback_data=f"save:{response_id}")]
    ])

    await message.reply(
        f"API Response: {response}",
        reply_markup=keyboard,  # Ensure the keyboard is passed here
    )


@dp.callback_query(lambda c: c.data and c.data.startswith("save:"))
async def save_callback_handler(callback_query: CallbackQuery) -> None:
    """Process the save button callback."""
    response_id = callback_query.data.split("save:")[1]

    # Retrieve the response from Redis
    response = await RedisService.get(f"response:{response_id}")

    if not response:
        await callback_query.message.answer("Error: Response not found or expired.")
        await callback_query.answer()  # Acknowledge the callback
        return

    # Process the response (e.g., save it to a database or perform another action)
    print(f"Response to save: {response}")
    # Simulate saving the response
    await callback_query.message.answer(f"Response '{response}' has been saved successfully.")
    await callback_query.answer()  # Acknowledge the callback
