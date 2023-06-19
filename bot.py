import logging
from aiogram import Bot, Dispatcher
from config import TOKEN

API_TOKEN = TOKEN   # your telegram bot token

# Initialize bot and dispatcher
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)