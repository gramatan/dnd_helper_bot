import sqlite3


def create_if_not_exist():
    conn = sqlite3.connect('dnd_bot.db')  # Creates a new db file if it doesn't exist
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS games
                 (chat_id INTEGER PRIMARY KEY, game_info TEXT)''')

    conn.commit()
    conn.close()