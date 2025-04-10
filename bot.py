import os
import asyncio
import signal
from telegram.ext import Application
from handlers import start_handler, echo_handler

# Main function to start the bot
async def main():
    token = os.environ.get("TELEGRAM_BOTTOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOTTOKEN environment variable is not set.")

    # Create the application
    application = Application.builder().token(token).build()

    # Add command and message handlers
    application.add_handler(start_handler)
    application.add_handler(echo_handler)

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
