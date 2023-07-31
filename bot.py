import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.middlewares import BaseMiddleware
from contextvars import ContextVar


from config import TOKEN

API_TOKEN = TOKEN   # your telegram bot token

ignore_log = ContextVar("ignore_log", default=False)


class LoggingMiddleware(BaseMiddleware):
    async def on_post_process_message(self, message: types.Message, *args):
        if not ignore_log.get():
            from db.utils import log_message
            log_message(message)
            logging.info(f"Message logged: {message.text}")


# Initialize bot and dispatcher
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
