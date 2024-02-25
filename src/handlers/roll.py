import re

from aiogram import types

from bot import handler_name
from utils.roll_utils import dx_roll, roll_dice


async def roll_dice_command(message: types.Message):
    handler_name.set('Roll')
    try:
        dice = int(message.text[6:])
    except ValueError:
        dice = 20

    roll, sides = dx_roll(dice)

    answer = f'd{sides}: {roll}'
    await message.reply(answer)


# main handler for expressions
async def dice_roll(message: types.Message):
    requests = re.findall(r'\b([+-]?\d*[dD]\d+[+-]?\d*|[dD])\b', message.text, re.IGNORECASE)
    if requests:
        handler_name.set('Auto')
        results = [f'{request}: {roll_dice(request)}' for request in requests]
        await message.reply('\n'.join(results))


async def stats_roll(message: types.Message):
    try:
        repeats = int(message.text.split()[1])
    except (IndexError, ValueError):
        repeats = 1

    best_stats = []
    best_sum = 0

    for _ in range(repeats):
        stats = []
        for _ in range(6):
            rolls = sorted([dx_roll(6)[0] for _ in range(4)], reverse=True)[:3]
            stats.append(sum(rolls))

        current_sum = sum(stats)
        if current_sum > best_sum:
            best_sum = current_sum
            best_stats = stats

    answer = f'Лучшие характеристики после {repeats} попыток: \n {best_stats}'

    await message.reply(answer)
