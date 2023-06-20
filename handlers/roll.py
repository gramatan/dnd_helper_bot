import re
import random

from aiogram import types

from bot import dp
from utils.roll_utils import dx_roll, roll_dice


@dp.message_handler(commands=['roll'])
async def roll_dice_command(message: types.Message):
    try:
        dice = int(message.text[6:])
    except ValueError:
        dice = 20

    roll, sides = dx_roll(dice)

    user = message.from_user.first_name
    answer = f"бросок d{sides} от {user}: {roll}"
    await message.answer(answer)


# main handler for expressions
@dp.message_handler()
async def dice_roll(message: types.Message):
    requests = re.findall(r'/([+-]?\d*[dD]\d+[+-]?\d*|[dD])', message.text, re.IGNORECASE)
    if requests:
        results = [f'/{request}: {roll_dice(request)}' for request in requests]
        await message.reply('\n'.join(results))
