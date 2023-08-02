import sqlite3
import logging

from datetime import datetime, timedelta


def log_message(message):
    from bot import handler_name
    handler = handler_name.get()
    if handler != '' and handler != 'Stats':
        conn = sqlite3.connect('dnd_bot.db')
        c = conn.cursor()
        is_private = 1 if message.chat.id > 0 else 0

        c.execute("INSERT INTO logs VALUES (?, ?, ?, ?)", (str(datetime.now()), message.from_user.id,
                                                           int(is_private), handler))
        conn.commit()
        conn.close()
        logging.debug(f"Message logged: {message.text}, handler: {handler}")


def get_week_stats():
    conn = sqlite3.connect('dnd_bot.db')
    c = conn.cursor()

    week_ago = datetime.now() - timedelta(days=7)
    query = f"""
    SELECT COUNT(DISTINCT user_id), COUNT(*)
    FROM logs
    WHERE date > '{week_ago.strftime('%Y-%m-%d %H:%M:%S')}'
    """
    c.execute(query)
    result = c.fetchone()

    conn.close()

    return result


def get_month_stats():
    conn = sqlite3.connect('dnd_bot.db')
    c = conn.cursor()

    month_ago = datetime.now() - timedelta(days=30)
    query = f"""
    SELECT COUNT(DISTINCT user_id), COUNT(*)
    FROM logs
    WHERE date > '{month_ago.strftime('%Y-%m-%d %H:%M:%S')}'
    """
    c.execute(query)
    result = c.fetchone()

    conn.close()

    return result


def get_top_5_requests():
    conn = sqlite3.connect('dnd_bot.db')
    c = conn.cursor()

    week_ago = datetime.now() - timedelta(days=7)
    query = f"""
    SELECT text, COUNT(*)
    FROM logs
    WHERE date > '{week_ago.strftime('%Y-%m-%d %H:%M:%S')}'
    GROUP BY text
    ORDER BY COUNT(*) DESC
    LIMIT 5
    """
    c.execute(query)
    result = c.fetchall()

    conn.close()

    return result


