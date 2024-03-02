import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import exceptions

from bot import bot
from database.utils import get_users


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


async def send_message(user_id: int, text: str, disable_notification: bool = True) -> bool:
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        logging.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        logging.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        logging.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)
    except exceptions.UserDeactivated:
        logging.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True
    return False


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
    elif query.data == 'broadcast_cancel':
        await query.message.answer("Broadcast canceled.")
    await state.finish()
