import sqlite3

import logging
import re
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import MessageNotModified


from func import roll_dice, dx_roll, make_character
from config import TOKEN
from keyboard import character_creation_keyboard
from masterdata import CLASSIC_CLASSES, CLASSES, RACES, CLASSIC_RACES, CLASSIC_STORIES, STORIES, WELCOME_MESSAGE
from db import create_if_not_exist

create_if_not_exist()
API_TOKEN = TOKEN   # your telegram bot token

# Initialize bot and dispatcher
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    welcome_message = WELCOME_MESSAGE
    await message.reply(welcome_message, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)


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


@dp.message_handler(commands=['class'])
async def class_list(message: types.Message):
    user = message.from_user.first_name
    if len(message.text) < 8:
        await message.reply(
            f"{user}, необходимо ввести слова для поиска после /class, орочья ты башка\n"
            "например:\n"
            "/class магический мастеровой\n"
            "/class рывок"
            )
    else:
        spell = message.text[7:]    # remove '/class ' part
        answer = (
            f"{user}, твоё заклинание где-то здесь:\n"
            f"[{spell}](https://dnd.su/class/?search={spell})"
        )
        await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)


@dp.message_handler(commands=['spell'])
async def spell_search(message: types.Message):
    user = message.from_user.first_name
    if len(message.text) < 8:
        await message.reply(
            f"{user}, ты забыл ввести слова для поиска после /spell\n"
            "например:\n"
            "/spell водоворот\n"
            "/spell Власть над водами"
            )
    else:
        spell = message.text[7:]    # remove '/spell ' part
        answer = (
            "твоё заклинание где-то здесь:\n"
            f"[{spell}](https://dnd.su/spells/?search={spell})"
        )
        await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)


@dp.message_handler(commands=['set'])
async def set_game(message: types.Message):
    chat_id = message.chat.id
    game_info = message.text[5:]  # Removes the '/set ' part

    conn = sqlite3.connect('dnd_bot.db')
    c = conn.cursor()

    # Insert or update game_info
    c.execute('''INSERT OR REPLACE INTO games (chat_id, game_info)
                 VALUES (?, ?)''', (chat_id, game_info))

    conn.commit()
    conn.close()

    await message.reply("Информация о следующей партии сохранена")


@dp.message_handler(commands=['game'])
async def get_game(message: types.Message):
    chat_id = message.chat.id

    conn = sqlite3.connect('dnd_bot.db')
    c = conn.cursor()

    # Retrieve game_info
    c.execute("SELECT game_info FROM games WHERE chat_id = ?", (chat_id,))
    game_info = c.fetchone()

    conn.close()

    if game_info is None:
        await message.reply("Информации о следующей игре нет. может быть вы забыли о команде /set?")
    else:
        await message.reply(game_info[0])


# character creation part
user_choices = {}  # global variable to store current user choices for character creation


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


@dp.message_handler(commands=['create_character'])
async def create_character(message: types.Message):
    reset_user_settings(message.chat.id)
    answer = generate_current_settings_message(message.chat.id)
    await bot.send_message(
        message.chat.id,
        answer,
        reply_markup=character_creation_keyboard()
    )


# add the reset functionality to the callback handler for 'reset_char' button
@dp.callback_query_handler(lambda c: c.data == 'reset_char')
async def reset_char_settings(callback_query: types.CallbackQuery):
    reset_user_settings(callback_query.from_user.id)  # Reset user settings
    answer = generate_current_settings_message(callback_query.from_user.id)  # Generate settings message after reset
    await bot.answer_callback_query(callback_query.id)
    try:
        await bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=answer,
            reply_markup=character_creation_keyboard()
        )
    except MessageNotModified:
        pass


# Handler for 'Пресет' button
@dp.callback_query_handler(lambda c: c.data == 'toggle_list')
async def toggle_list(callback_query: types.CallbackQuery):
    # Get current choice
    chat_id = callback_query.message.chat.id
    user_choice = user_choices.setdefault(chat_id, {})
    preset = user_choice.get('preset', 'Классика')
    # Toggle preset
    preset = 'Расширенный' if preset == 'Классика' else 'Классика'
    user_choice['preset'] = preset
    # Update message and keyboard
    await bot.edit_message_text(
        generate_current_settings_message(chat_id),
        chat_id,
        callback_query.message.message_id,
        reply_markup=character_creation_keyboard())


# Handler for 'Класс' button
@dp.callback_query_handler(lambda c: c.data == 'select_class')
async def select_class(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_choice = user_choices.setdefault(chat_id, {})
    preset = user_choice.get('preset', 'Классика')
    classes = CLASSIC_CLASSES if preset == 'Классика' else CLASSES
    keyboard = InlineKeyboardMarkup(row_width=3)
    for class_name in classes:
        button = InlineKeyboardButton(class_name, callback_data=f'selected_class_{class_name}')
        keyboard.insert(button)

    await bot.edit_message_text(
        'Выберите класс:',
        chat_id,
        callback_query.message.message_id,
        reply_markup=keyboard
    )


# Handler for when a class is selected
@dp.callback_query_handler(lambda c: c.data.startswith('selected_class_'))
async def selected_class(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_choice = user_choices.setdefault(chat_id, {})
    class_name = callback_query.data[len('selected_class_'):]

    # Update user choice
    user_choice['char_class'] = class_name

    # Update message and keyboard
    await bot.edit_message_text(
        generate_current_settings_message(chat_id),
        chat_id,
        callback_query.message.message_id,
        reply_markup=character_creation_keyboard()
    )


# Handler for 'раса' button
@dp.callback_query_handler(lambda c: c.data == 'select_race')
async def select_race(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_choice = user_choices.setdefault(chat_id, {})
    preset = user_choice.get('preset', 'Классика')
    races = CLASSIC_RACES if preset == 'Классика' else RACES
    keyboard = InlineKeyboardMarkup(row_width=3)
    for race_name in races:
        button = InlineKeyboardButton(race_name, callback_data=f'selected_race_{race_name}')
        keyboard.insert(button)

    await bot.edit_message_text(
        'Выберите расу:',
        chat_id,
        callback_query.message.message_id,
        reply_markup=keyboard
    )


# Handler for when a race is selected
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('selected_race_'))
async def select_race_choice(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_choice = user_choices.setdefault(chat_id, {})
    race_name = callback_query.data[len('selected_race_'):]

    # Update user choice
    user_choice['char_race'] = race_name

    # Update message and keyboard
    await bot.edit_message_text(
        generate_current_settings_message(chat_id),
        chat_id,
        callback_query.message.message_id,
        reply_markup=character_creation_keyboard()
    )


# Handler for 'История' button
@dp.callback_query_handler(lambda c: c.data == 'select_story')
async def select_story(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_choice = user_choices.setdefault(chat_id, {})
    preset = user_choice.get('preset', 'Классика')
    stories = CLASSIC_STORIES if preset == 'Классика' else STORIES
    keyboard = InlineKeyboardMarkup(row_width=3)
    for story_name in stories:
        button = InlineKeyboardButton(story_name, callback_data=f'selected_story_{story_name}')
        keyboard.insert(button)

    await bot.edit_message_text(
        'Выберите предысторию:',
        chat_id,
        callback_query.message.message_id,
        reply_markup=keyboard
    )


# Handler for when a story is selected
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('selected_story_'))
async def select_story_choice(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_choice = user_choices.setdefault(chat_id, {})
    story_name = callback_query.data[len('selected_story_'):]

    # Update user choice
    user_choice['char_story'] = story_name

    # Update message and keyboard
    await bot.edit_message_text(
        generate_current_settings_message(chat_id),
        chat_id,
        callback_query.message.message_id,
        reply_markup=character_creation_keyboard()
    )


# Handler for 'Количество персонажей' button
@dp.callback_query_handler(lambda c: c.data == 'select_num_chars')
async def select_num_chars(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id

    # Create keyboard for selecting number of characters
    keyboard = InlineKeyboardMarkup(row_width=5)
    for i in range(1, 11):
        button = InlineKeyboardButton(str(i), callback_data=f'selected_num_chars_{i}')
        keyboard.insert(button)

    await bot.edit_message_text(
        'Выберите количество персонажей:',
        chat_id,
        callback_query.message.message_id,
        reply_markup=keyboard
    )


# Handler for when a number of characters is selected
@dp.callback_query_handler(lambda c: c.data.startswith('selected_num_chars_'))
async def selected_num_chars(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_choice = user_choices.setdefault(chat_id, {})
    num_chars = int(callback_query.data[len('selected_num_chars_'):])

    # Update user choice
    user_choice['num_chars'] = num_chars

    # Update message and keyboard
    await bot.edit_message_text(
        generate_current_settings_message(chat_id),
        chat_id,
        callback_query.message.message_id,
        reply_markup=character_creation_keyboard()
    )


# Handler for 'Создать' button
@dp.callback_query_handler(lambda c: c.data == 'generate')
async def generate(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_choice = user_choices.get(chat_id, {})
    # Get choices
    preset = user_choice.get('preset', 'Классика')
    char_class = user_choice.get('char_class', 'Случайно')
    race = user_choice.get('char_race', 'Случайно')
    story = user_choice.get('char_story', 'Случайно')
    num_chars = user_choice.get('num_chars', 3)
    # Generate characters
    characters = '\n---\n'.join(make_character(char_class, race, story, preset == 'Классика') for _ in range(num_chars))
    # Send characters
    await bot.send_message(chat_id, characters, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)


# main handler for expressions
@dp.message_handler()
async def dice_roll(message: types.Message):
    requests = re.findall(r'/([+-]?\d*[dD]\d+[+-]?\d*|[dD])', message.text, re.IGNORECASE)
    if requests:
        results = [f'/{request}: {roll_dice(request)}' for request in requests]
        await message.reply('\n'.join(results))


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=False)
