from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters

class EchoHandler:
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(update.message.text)

    def get_handler(self):
        return MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle)
