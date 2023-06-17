from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def character_creation_keyboard():
    keyboard = InlineKeyboardMarkup()

    # Button to toggle between classic and expanded list
    toggle_list = InlineKeyboardButton('Пресет', callback_data='toggle_list')

    # Buttons for class, race and story
    select_class = InlineKeyboardButton('Класс', callback_data='select_class')
    select_race = InlineKeyboardButton('Раса', callback_data='select_race')
    select_story = InlineKeyboardButton('История', callback_data='select_story')

    # Button for inputting number of variants
    select_variants = InlineKeyboardButton('Количество', callback_data='select_variants')

    # Button for generating character
    generate_button = InlineKeyboardButton('Создать', callback_data='generate')

    # Add buttons to keyboard
    keyboard.add(toggle_list, select_class, select_race, select_story, select_variants, generate_button)

    return keyboard
