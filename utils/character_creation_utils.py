import random

from utils.masterdata import CLASSIC_ITEMS, EXTENDED_ITEMS, CLASS_LINK, RACE_LINK, STORY_LINK

user_choices = {}  # global variable to store current user choices for character creation


def select_item(choices, user_choice):
    # Check if user choice exists and is valid
    if user_choice and user_choice in choices:
        item_link = choices[user_choice]
    else:
        user_choice, item_link = random.choice(list(choices.items()))
    return user_choice, item_link


def make_character(char_class='', char_race='', char_story='', classic=False) -> str:
    items = CLASSIC_ITEMS if classic else EXTENDED_ITEMS

    char_class, class_link = select_item(items['char_class'], char_class)
    char_race, race_link = select_item(items['char_race'], char_race)
    char_story, story_link = select_item(items['char_story'], char_story)

    class_link = CLASS_LINK + class_link + '/'
    race_link = RACE_LINK + race_link + '/'
    story_link = STORY_LINK + story_link + '/'

    return (
        f"[{char_class}]({class_link})\n"
        f"[{char_race}]({race_link})\n"
        f"[{char_story}]({story_link})\n"
    )


def generate_current_settings_message(chat_id):
    user_choice = user_choices.get(chat_id, {})
    preset = user_choice.get('preset', 'Классика')
    char_class = user_choice.get('char_class', 'Случайно')
    char_race = user_choice.get('char_race', 'Случайно')
    char_story = user_choice.get('char_story', 'Случайно')
    num_chars = user_choice.get('num_chars', 3)

    return (
        f"Время создать персонажа! Текущие параметры:\n"
        f"Пресет: {preset}\n"
        f"Класс: {char_class}\n"
        f"Раса: {char_race}\n"
        f"Предыстория: {char_story}\n"
        f"Количество персонажей: {num_chars}\n"
    )


def reset_user_settings(chat_id):
    user_choices[chat_id] = {
        "preset": "Классика",
        "char_class": "Случайно",
        "char_race": "Случайно",
        "char_story": "Случайно",
        "num_chars": 3
    }
