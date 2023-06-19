from bot import dp
from db.db import create_if_not_exist

# Import handlers
# "roll" should be the last one,
# because it has a catch-all handler

create_if_not_exist()

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=False)
