from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

class StartHandler:
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hello! I am your bot. How can I assist you?")

    def get_handler(self):
        return CommandHandler("start", self.handle)
