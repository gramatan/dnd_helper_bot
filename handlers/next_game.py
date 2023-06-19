import sqlite3

from aiogram import types

from bot import dp


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
