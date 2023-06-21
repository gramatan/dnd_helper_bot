from aiogram import types

from bot import dp


async def class_list(message: types.Message):
    user = message.from_user.first_name
    if len(message.text) < 8:
        await message.reply(
            f"{user}, необходимо ввести слова для поиска после /class, орочья ты башка\n"
            "например:\n"
            "/class магический мастеровой\n"
            "/class рывок"
            )
    else:
        spell = message.text[7:]    # remove '/class ' part
        answer = (
            f"{user}, твоё заклинание где-то здесь:\n"
            f"[{spell}](https://dnd.su/class/?search={spell})"
        )
        await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)


async def spell_search(message: types.Message):
    user = message.from_user.first_name
    if len(message.text) < 8:
        await message.reply(
            f"{user}, ты забыл ввести слова для поиска после /spell\n"
            "например:\n"
            "/spell водоворот\n"
            "/spell Власть над водами"
            )
    else:
        spell = message.text[7:]    # remove '/spell ' part
        answer = (
            "твоё заклинание где-то здесь:\n"
            f"[{spell}](https://dnd.su/spells/?search={spell})"
        )
        await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)
