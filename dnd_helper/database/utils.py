import logging
from datetime import datetime, timedelta

from aiogram import types

from dnd_helper.database.db import database_connection


def log_message(message: types.Message):
    from dnd_helper.bot import handler_name
    handler = handler_name.get()
    if handler != '' and handler != 'Stats':
        with database_connection(commit=True) as cursor:
            is_private = 1 if message.chat.id > 0 else 0

            cursor.execute('INSERT INTO logs VALUES (?, ?, ?, ?)', (
                str(datetime.now()),
                message.from_user.id,
                int(is_private),
                handler,
            ))
            logging.debug(f'Message logged: {message.text}, handler: {handler}')


def get_unique_users_count():
    with database_connection() as cursor:
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
    return count


def get_week_stats():
    with database_connection() as cursor:
        week_ago = datetime.now() - timedelta(days=7)
        query = f"""
        SELECT COUNT(DISTINCT user_id), COUNT(*)
        FROM logs
        WHERE date > '{week_ago.strftime('%Y-%m-%d %H:%M:%S')}'
        """
        cursor.execute(query)
        result = cursor.fetchone()

    return result


def get_month_stats():
    with database_connection() as cursor:

        month_ago = datetime.now() - timedelta(days=30)
        query = f"""
        SELECT COUNT(DISTINCT user_id), COUNT(*)
        FROM logs
        WHERE date > '{month_ago.strftime('%Y-%m-%d %H:%M:%S')}'
        """
        cursor.execute(query)
        result = cursor.fetchone()

    return result


def get_top_5_requests():
    with database_connection() as cursor:
        week_ago = datetime.now() - timedelta(days=7)
        query = f"""
        SELECT text, COUNT(*)
        FROM logs
        WHERE date > '{week_ago.strftime('%Y-%m-%d %H:%M:%S')}'
        GROUP BY text
        ORDER BY COUNT(*) DESC
        LIMIT 5
        """
        cursor.execute(query)
        result = cursor.fetchall()

    return result


def db_set_game(chat_id: str, game_info: str):
    with database_connection(commit=True) as cursor:
        cursor.execute('''INSERT OR REPLACE INTO games (chat_id, game_info)
                     VALUES (?, ?)''', (chat_id, game_info))


def db_get_game(chat_id: int):
    with database_connection(commit=True) as cursor:
        cursor.execute('SELECT game_info FROM games WHERE chat_id = ?', (chat_id,))
        game_info = cursor.fetchone()
    return game_info


def get_users():
    with database_connection() as cursor:
        cursor.execute("SELECT user_id FROM users WHERE is_subscribed = 1")
        return [row[0] for row in cursor.fetchall()]


def save_user(user_id, is_subscribed=True):
    try:
        with database_connection(commit=True) as cursor:
            cursor.execute("INSERT OR REPLACE INTO users (user_id, is_subscribed) VALUES (?, ?)",
                           (user_id, int(is_subscribed)))
    except Exception as ex:
        logging.exception(f'Failed to save or update user information with error: {ex}')


def add_or_check_user_prayer(user_id):
    with database_connection(commit=True) as cursor:
        cursor.execute("SELECT blocked FROM prayers WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO prayers (user_id, blocked) VALUES (?, 0)", (user_id,))
            return "new_user"
        elif result[0] == 1:
            return "blocked_user"
        else:
            return "existing_user"


def block_user_prayer(user_id):
    with database_connection(commit=True) as cursor:
        cursor.execute("UPDATE prayers SET blocked = 1 WHERE user_id = ?", (user_id,))
