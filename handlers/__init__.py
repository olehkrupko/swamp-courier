from telegram.ext import CommandHandler, MessageHandler, filters
from .start_handler import StartHandler
from .echo_handler import EchoHandler

# Instantiate handler classes
start_handler = StartHandler().get_handler()
echo_handler = EchoHandler().get_handler()

# Export handlers
__all__ = ["start_handler", "echo_handler"]
