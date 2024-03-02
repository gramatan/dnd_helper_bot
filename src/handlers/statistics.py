import csv
import sqlite3

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import handler_name
from database.utils import (
    get_month_stats,
    get_top_5_requests,
    get_week_stats,
    get_unique_users_count,
)


def export_logs_to_csv():
    conn = sqlite3.connect('db/dnd_bot.db')
    c = conn.cursor()

    c.execute('SELECT * FROM logs')
    result = c.fetchall()

    with open('logs.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['date', 'user_id', 'is_private', 'text'])
        writer.writerows(result)

    conn.close()

    return 'logs.csv'

def export_users_to_csv():
    conn = sqlite3.connect('db/dnd_bot.db')
    c = conn.cursor()

    c.execute('SELECT * FROM users')
    result = c.fetchall()

    with open('users.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['user_id', 'is_subscribed'])
        writer.writerows(result)

    conn.close()

    return 'users.csv'

async def stats_command(message: types.Message):
    handler_name.set('Stats')
    week_users, week_messages = get_week_stats()
    month_users, month_messages = get_month_stats()
    top_requests = get_top_5_requests()
    users_from_user_table = get_unique_users_count()

    top_requests_text = '\n'.join([f'{request[0]}: {request[1]}' for request in top_requests])

    week_stat = (
        f'This week:\n'
        f'Unique: {week_users}\n'
        f'Requests: {week_messages}\n\n'
    )
    month_stat = (
        f'Last 30 days:\n'
        f'Unique: {month_users}\n'
        f'Requests: {month_messages}\n\n'
    )
    top_requests_stat = (
        f'Top 5 last week:\n'
        f'{top_requests_text}\n\n'
    )

    registered = (
        f'Total unique users: {users_from_user_table}'
    )

    text = week_stat + month_stat + top_requests_stat + registered
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton('Download logs', callback_data='statistics_csv'),
        InlineKeyboardButton('Download users', callback_data='statistics_users'),
    )
    await message.reply(text, reply_markup=keyboard)


async def on_csv_button(call: types.CallbackQuery):
    if call.data == 'statistics_csv':
        filename = export_logs_to_csv()
        with open(filename, 'rb') as file:
            await call.message.answer_document(file, caption='CSV file with logs')
        await call.answer()
    elif call.data == 'statistics_users':
        filename = export_users_to_csv()
        with open(filename, 'rb') as file:
            await call.message.answer_document(file, caption='CSV file with users')
        await call.answer()
