import logging
import re
from aiogram import Bot, Dispatcher, types

from func import roll_dice, dx_roll
from config import TOKEN
import sqlite3

conn = sqlite3.connect('dnd_bot.db')  # Creates a new db file if it doesn't exist
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS games
             (chat_id INTEGER PRIMARY KEY, game_info TEXT)''')

conn.commit()
conn.close()

API_TOKEN = TOKEN   # your telegram bot token

# Initialize bot and dispatcher
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    welcome_message = (
        "Привет! Я бот, который может помочь в ваших DnD приключениях, бросая кости за вас. "
        "Просто отправьте сообщение в формате '/NdM+K', где N - количество кубиков, "
        "M - количество граней на кубике, K - модификатор (необязательно). Например, /2d20+5'. "
        "Я вычислю результат для вас!\n\n"
        "Вы также можете использовать команду /roll N, где N - это количество сторон на кубике "
        "(по умолчанию 20, если N не указано). "
        "Это простой способ быстро бросить один кубик. Например, /roll 100 бросит 100-гранный кубик за вас.\n\n"
        "Вы также можете установить информацию о следующей игре с помощью команды /set, "
        "а потом получить ее обратно с помощью команды /game.\n\n"
        "Если вы хотите найти описание заклинания, просто используйте команду /spell Название заклинания.\n"
        "Для поиска по справочнику классов, используйте команду /class Название навыка.\n\n"
        "Вот список сайтов, которые могут помочь:\n"
        "[DnD.su. Справочник по заклинаниям](https://dnd.su/spells/)\n"  
        "[DnD.su. Справочник по классам](https://dnd.su/class/)\n"
        "[DnD.su. Справочник по расам](https://dnd.su/race/)\n\n"
        "[Интерактивный чарлист](https://longstoryshort.app/characters/list/)\n\n"
        "[Правила для начинающих игроков](https://www.dungeonsanddragons.ru/bookfull/5ed/5e%20starter%20set%20-%20basic%20rules%20RUS.pdf)\n"
        "[Миниатюры персонажей Hero Forge](https://www.heroforge.com/)\n"
    )

    await message.reply(welcome_message, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)


@dp.message_handler(commands=['roll'])
async def roll_dice_command(message: types.Message):
    # print(message.text)
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


@dp.message_handler()
async def dice_roll(message: types.Message):
    requests = re.findall(r'/(.*?)(?=\s|$|[^0-9dD+-])', message.text, re.IGNORECASE)
    if requests and all('d' in req or 'D' in req for req in requests):
        results = [f'/{request}: {roll_dice(request)}' for request in requests]
        await message.reply('\n'.join(results))


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
