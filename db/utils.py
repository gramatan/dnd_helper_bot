import datetime
import sqlite3


def log_message(message):
    conn = sqlite3.connect('dnd_bot.db')
    c = conn.cursor()
    is_private = 1 if message.chat.id > 0 else 0
    c.execute("INSERT INTO logs VALUES (?, ?, ?, ?)", (str(datetime.datetime.now()), message.from_user.id,
                                                       int(is_private), message.text))
    conn.commit()
    conn.close()
