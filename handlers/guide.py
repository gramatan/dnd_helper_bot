from aiogram import types


async def class_search(message: types.Message):
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
            f"{user}, попробуй поискать тут:\n"
            f"[{spell}](https://dnd.su/class/?search={spell})"
        )
        await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)


async def item_search(message: types.Message):
    user = message.from_user.first_name
    if len(message.text) < 8:
        await message.reply(
            f"{user}, это поиск вещей, необходимо ввести слова для поиска после /item\n"
            "например:\n"
            "/item жемчужина силы\n"
            "/item посох защиты "
            )
    else:
        spell = message.text[6:]    # remove '/item ' part
        answer = (
            f"{user}, для поиска пройди по ссылке:\n"
            f"[{spell}](https://dnd.su/items/?search={spell})"
        )
        await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)


async def mech_search(message: types.Message):
    user = message.from_user.first_name
    if len(message.text) < 8:
        await message.reply(
            f"{user}, это поиск! чтобы что-то поискать, нужно что-то поискать.\n"
            "необходимо ввести слова для поиска после /mech\n"
            "например:\n"
            "/mech безумие\n"
            "/mech языки"
            )
    else:
        spell = message.text[6:]    # remove '/mech ' part
        answer = (
            f"{user}, то что ты ищешь находится здесь:\n"
            f"[{spell}](https://dnd.su/mechanics/?search={spell})"
        )
        await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)
