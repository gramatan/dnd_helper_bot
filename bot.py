import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.middlewares import BaseMiddleware
from contextvars import ContextVar

from config import TOKEN

API_TOKEN = TOKEN   # your telegram bot token

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

handler_name = ContextVar("handler_name", default="")


class LoggingMiddleware(BaseMiddleware):
    async def on_post_process_message(self, message: types.Message, *args):
        from database.utils import log_message
        log_message(message)


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
