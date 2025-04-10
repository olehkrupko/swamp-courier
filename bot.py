import os
import asyncio
import signal
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Command handler for the /start command
async def start(update: Update, context):
    await update.message.reply_text("Hello! I am your bot. How can I assist you?")

# Echo handler for all text messages
async def echo(update: Update, context):
    await update.message.reply_text(update.message.text)

# Main function to start the bot
async def main():
    token = os.environ.get("TELEGRAM_BOTTOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOTTOKEN environment variable is not set.")

    # Create the application
    application = Application.builder().token(token).build()

    # Add command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Graceful shutdown handling
    async def shutdown():
        print("Shutting down bot...")
        await application.shutdown()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown()))

    # Start the bot
    print("Bot is running...")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
