import re
import random


def roll_dice(expression):
    # Prevent huge numbers
    if any(int(num) > 100 for num in re.findall(r'\d+', expression)):
        return '¯\_(ツ)_/¯ для больших чисел используй /roll'

    parts = re.findall(r'([+-]?)(\d*)[dD](\d+)?|([+-]\d+)', expression, re.IGNORECASE)
    rolls = []
    total = 0
    for part in parts:
        sign, dice, sides, const = part
        sign = -1 if sign == '-' else 1
        if dice or sides:
            dice = int(dice) if dice else 1
            sides = int(sides) if sides else 1  # Default to 1 if no sides specified (e.g., "+5" or "-5")
            for _ in range(dice):
                roll = sign * random.randint(1, sides)
                rolls.append(str(roll))
                total += roll
        if const:  # If there is a constant modifier, add or subtract it from the total
            total += sign * int(const)
            rolls.append(str(sign * int(const)))
    return f'{"+".join(rolls)} = {total}' if len(rolls) > 1 else f'{total}'


def dx_roll(sides=20):
    if sides > 100000:
        sides = 20
    roll = random.randint(1, sides)
    return roll, sides
