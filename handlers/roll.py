import re
import random

from aiogram import types

from bot import dp


def roll_dice(expression):
    # Special case for /d or /D
    if expression.lower() == 'd':
        return f'{random.randint(1, 20)} of 20'

    # Check for numbers larger than 1000
    if any(int(num) > 1000 for num in re.findall(r'\d+', expression)):
        return '¯\_(ツ)_/¯ для больших чисел используй /roll'

    parts = re.findall(r'([+-]?)(\d*)[dD](\d+)?|([+-]\d+)', expression, re.IGNORECASE)
    rolls = []
    total = 0

    for part in parts:
        sign, dice, sides, const = part
        sign = -1 if sign == '-' else 1

        if dice or sides:
            dice = max(int(dice) if dice else 1, 1)  # At least one dice
            sides = int(sides) if sides else 20  # Default to 20 sides if no sides specified (e.g., "+5" or "-5")
            for _ in range(dice):
                roll = sign * random.randint(1, sides)
                rolls.append(str(roll))
                total += roll

        if const:  # If there is a constant modifier, add or subtract it from the total
            total += sign * int(const)
            rolls.append(str(sign * int(const)))

    return f'{"+".join(rolls)} = {total}' if len(rolls) > 1 else f'{total}'


def dx_roll(sides=20) -> tuple:
    if sides > 100000:
        sides = 20
    roll = random.randint(1, sides)
    return roll, sides


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
