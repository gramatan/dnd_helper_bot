import re

from aiogram import types

from bot import ignore_log
from utils.roll_utils import dx_roll, roll_dice


async def roll_dice_command(message: types.Message):
    try:
        dice = int(message.text[6:])
    except ValueError:
        dice = 20

    roll, sides = dx_roll(dice)

    answer = f"d{sides}: {roll}"
    await message.reply(answer)


# main handler for expressions
async def dice_roll(message: types.Message):
    requests = re.findall(r'\b([+-]?\d*[dD]\d+[+-]?\d*|[dD])\b', message.text, re.IGNORECASE)
    if requests:
        results = [f'{request}: {roll_dice(request)}' for request in requests]
        await message.reply('\n'.join(results))
    else:
        ignore_log.set(True)
