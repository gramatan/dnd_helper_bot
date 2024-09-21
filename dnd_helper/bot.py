import logging
from contextvars import ContextVar

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.middlewares import BaseMiddleware
from config import TOKEN

API_TOKEN = TOKEN   # your telegram bot token

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

handler_name = ContextVar('handler_name', default='')


class LoggingMiddleware(BaseMiddleware):
    async def on_post_process_message(self, message: types.Message, *args):
        from database.utils import log_message, save_user
        log_message(message)
        save_user(message.from_user.id)


# Initialize storage, bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
