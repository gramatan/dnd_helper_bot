import sqlite3
import csv

from datetime import datetime, timedelta


def log_message(message):
    conn = sqlite3.connect('dnd_bot.db')
    c = conn.cursor()
    is_private = 1 if message.chat.id > 0 else 0
    c.execute("INSERT INTO logs VALUES (?, ?, ?, ?)", (str(datetime.now()), message.from_user.id,
                                                       int(is_private), message.text))
    conn.commit()
    conn.close()


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


def export_to_csv():
    conn = sqlite3.connect('dnd_bot.db')
    c = conn.cursor()

    c.execute("SELECT * FROM logs")
    result = c.fetchall()

    with open('logs.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['date', 'user_id', 'is_private', 'text'])
        writer.writerows(result)

    conn.close()

    return 'logs.csv'
