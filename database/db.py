import logging
import sqlite3


def create_if_not_exist():
    try:
        conn = sqlite3.connect('./db/dnd_bot.db')  # Creates a new db file if it doesn't exist
        c = conn.cursor()

        # Create table games
        c.execute('''CREATE TABLE IF NOT EXISTS games
                     (chat_id INTEGER PRIMARY KEY, game_info TEXT)''')
        conn.commit()

        # Create table logs
        c.execute(
            '''CREATE TABLE IF NOT EXISTS logs 
            (date text, user_id text, is_private integer, text text)''')
        conn.commit()
        conn.close()
        logging.info("Database created successfully")
    except Exception as e:
        print(f"Error occurred: {e}")
