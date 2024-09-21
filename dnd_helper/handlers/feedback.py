from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from dnd_helper.database.utils import add_or_check_user_prayer, block_user_prayer
from dnd_helper.utils.message_sender import send_message
from dnd_helper.bot import handler_name, bot
from dnd_helper.config import ADMIN_ID


class FeedbackStates(StatesGroup):
    waiting_for_message = State()


async def get_feedback(message: types.Message):
    handler_name.set('feedback')
    if len(message.text) < 10:
        await message.reply(
            'Молитва создателю должна быть после /feedback\n'
            'например:\n'
            '/feedback На сайте появились новые заклинания, а у тебя их нет! '
            'например "могучая вспышка"'
        )
    else:
        user_status = add_or_check_user_prayer(message.from_user.id)
        if user_status == "blocked_user":
            await message.reply("Твоя молитва не была услышана.")
            return
        feedback_text = message.text[9:]
        sender = str(message.from_user.username)
        sender_id = str(message.from_user.id)
        text = (
            f'Пользователь `{sender}` (`{sender_id}`) отправил сообщение:\n\n'
            f'Текст сообщения:\n`{feedback_text}`'
        )
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(text="Delete", callback_data=f"feedback_done:{sender_id}"),
            InlineKeyboardButton(text="Reply", callback_data=f"feedback_reply:{sender_id}"),
            InlineKeyboardButton(text="Block", callback_data=f"feedback_block:{sender_id}")
        )
        await send_message(
            user_id=ADMIN_ID,
            text=text,
            parse_mode=types.ParseMode.MARKDOWN,
            reply_markup=keyboard,
            disable_notification=True,
        )
        await message.reply(f'Сообщение отправлено.\n{message.text[9:]}')
        await message.delete()


async def feedback_callback_handler(query: types.CallbackQuery, state: FSMContext):
    user_id = query.data.split(":")[1]
    if query.data.startswith('feedback_done:'):
        await bot.delete_message(chat_id=ADMIN_ID, message_id=query.message.message_id)
        await query.answer("Feedback deleted.")
    elif query.data.startswith('feedback_reply:'):
        await state.set_state(FeedbackStates.waiting_for_message)
        await state.update_data(reply_to_user_id=user_id)
        await query.message.answer("Please type your reply.")
    elif query.data.startswith('feedback_block:'):
        user_id = query.data.split(":")[1]
        block_user_prayer(user_id)
        await bot.delete_message(chat_id=ADMIN_ID, message_id=query.message.message_id)
        await query.answer("User blocked.")


async def reply_feedback_handler(query: types.CallbackQuery, state: FSMContext):
    sender_id = query.data.split(":")[1]
    await state.set_state(FeedbackStates.waiting_for_reply)
    await state.update_data(reply_to_user_id=sender_id)
    await query.message.answer("Please type your reply.")


async def feedback_reply_message_handler(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    reply_to_user_id = state_data.get("reply_to_user_id")
    if reply_to_user_id:
        await send_message(int(reply_to_user_id), message.text)
        await message.answer("Reply sent.")
    await state.finish()
