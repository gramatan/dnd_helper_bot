import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from dnd_helper.bot import bot
from dnd_helper.config import ADMIN_ID
from dnd_helper.database.utils import get_users
from dnd_helper.utils.message_sender import send_message


class BroadcastStates(StatesGroup):
    waiting_for_message = State()


async def start_broadcast_command(message: types.Message):
    await BroadcastStates.waiting_for_message.set()
    logging.info(f"State set to: {BroadcastStates.waiting_for_message}")
    await message.answer("Send me a message for broadcast.")


async def message_handler(message: types.Message, state: FSMContext):
    logging.info("message_handler is called")
    if message.text is not None:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("Send", callback_data="broadcast_send"),
            InlineKeyboardButton("Cancel", callback_data="broadcast_cancel"),
        )
        await state.update_data(broadcast_message=message.text)
        await message.answer(f"message:\n\n{message.text}", reply_markup=keyboard)


async def broadcaster(message: str) -> int:
    count = 0
    users = get_users()
    for user_id in users:
        if await send_message(user_id, message):
            count += 1
        await asyncio.sleep(.05)
    logging.info(f"{count} messages successful sent.")
    return count


async def broadcast_callback_handler(query: types.CallbackQuery, state: FSMContext):
    if query.data == 'broadcast_send':
        data = await state.get_data()
        if 'broadcast_message' in data:
            count = await broadcaster(data['broadcast_message'])
            await query.message.answer(f'Broadcast done for {count} users.')
            await bot.delete_message(chat_id=ADMIN_ID, message_id=query.message.message_id)
    elif query.data == 'broadcast_cancel':
        await query.message.answer("Broadcast canceled.")
        await bot.delete_message(chat_id=ADMIN_ID, message_id=query.message.message_id)
    await state.finish()
