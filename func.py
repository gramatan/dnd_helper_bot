import re
import random
from masterdata import CLASSES, CLASSIC_CLASSES, RACES, CLASSIC_RACES, STORIES
from masterdata import CLASSIC_STORIES, CLASS_LINK, RACE_LINK, STORY_LINK


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


def make_character(char_class='', char_race='', char_story='', classic=False) -> str:
    if not char_class or char_class not in CLASSES:
        if not classic:
            char_class, class_link = random.choice(list(CLASSES.items()))
        else:
            char_class, class_link = random.choice(list(CLASSIC_CLASSES.items()))
    else:
        class_link = CLASSES[char_class]

    if not char_race or char_race not in RACES:
        if not classic:
            char_race, race_link = random.choice(list(RACES.items()))
        else:
            char_race, race_link = random.choice(list(CLASSIC_RACES.items()))
    else:
        race_link = RACES[char_race]
    if not char_story or char_story not in STORIES:
        if not classic:
            char_story, story_link = random.choice(list(STORIES.items()))
        else:
            char_story, story_link = random.choice(list(CLASSIC_STORIES.items()))
    else:
        story_link = STORIES[char_story]

    class_link = CLASS_LINK + class_link + '/'
    race_link = RACE_LINK + race_link + '/'
    story_link = STORY_LINK + story_link + '/'

    return (
        f"[{char_class}]({class_link})\n"
        f"[{char_race}]({race_link})\n"
        f"[{char_story}]({story_link})\n"
    )


# for i in range(5):
#     print(make_character(classic=False))
#     print('---')
