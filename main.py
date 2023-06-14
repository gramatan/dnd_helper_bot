import logging
import re
import random
from aiogram import Bot, Dispatcher, types

from func import roll_dice
from config import TOKEN

API_TOKEN = TOKEN

# Initialize bot and dispatcher
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I'm a dice rolling bot. Send me a message like '1d20' or '2d4+2' to roll dice.")


@dp.message_handler()
async def dice_roll(message: types.Message):
    requests = re.findall('([+-]?\d*d\d+[+-]?\d*|[+-]\d+)', message.text)
    if requests:
        results = [f'{request}: {roll_dice(request)}' for request in requests]
        await message.reply('\n'.join(results))


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
