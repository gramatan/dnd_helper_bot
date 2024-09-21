import asyncio
import logging

from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils import exceptions

from dnd_helper.bot import bot


async def send_message(
        user_id: int,
        text: str,
        parse_mode: types.ParseMode = None,
        reply_markup: InlineKeyboardMarkup = None,
        disable_notification: bool = True,
) -> bool:
    try:
        await bot.send_message(
            user_id,
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            disable_notification=disable_notification,
        )
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
