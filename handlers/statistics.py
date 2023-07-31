from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.utils import get_week_stats, get_month_stats, export_to_csv

async def stats_command(message: types.Message):
    week_users, week_messages = get_week_stats()
    month_users, month_messages = get_month_stats()

    text = f"""
    This week:
    Unique: {week_users}
    Requests: {week_messages}
    
    Last 30 days:
    Unique: {month_users}
    Requests: {month_messages}
    """

    csv_button = InlineKeyboardMarkup().add(InlineKeyboardButton("Download CSV", callback_data="csv"))
    await message.reply(text, reply_markup=csv_button)


async def on_csv_button(call: types.CallbackQuery):
    if call.data == "csv":
        filename = export_to_csv()
        with open(filename, 'rb') as file:
            await call.message.answer_document(file, caption="CSV file with logs")
        await call.answer()
