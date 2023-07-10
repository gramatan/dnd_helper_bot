from aiogram import types

from bot import dp


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
            f"{user}, твоё заклинание где-то здесь:\n"
            f"[{spell}](https://dnd.su/class/?search={spell})"
        )
        await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)


async def spell_search(message: types.Message):
    from main import spell_cards
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
        spell_lower = spell.lower()
        matches = [key for key in spell_cards.keys() if spell_lower in key]

        if len(matches) == 1:
            card = spell_cards[matches[0]]
            details = {
                "Время накладывания": card.casting_time,
                "Дистанция": card.c_range,
                "Компоненты": card.components,
                "Длительность": card.duration,
                "Классы": card.classes,
                "Архетипы": card.archetypes,
                # "Источник": card.source,
            }

            details_text = "\n".join([f"{key}: {value}" for key, value in details.items() if value is not None])

            answer = f"**{card.title}** ({card.title_en})\n\n" \
                     f"{card.level_school}\n" \
                     f"{details_text}\n\n" \
                     f"{card.description}\n\n" \
                     f"[Ссылка на DnD.su](https://dnd.su{card.link})"

        else:
            answer = (
                "твоё заклинание где-то здесь:\n"
                f"[{spell}](https://dnd.su/spells/?search={spell})"
            )

        await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)


async def bestiary_search(message: types.Message):
    user = message.from_user.first_name
    if len(message.text) < 8:
        await message.reply(
            f"{user}, никак ты не научишься, необходимо ввести слова для поиска после /bestiary\n"
            "например:\n"
            "/bestiary Багбиры\n"
            "/bestiary Вегепигмеи "
            )
    else:
        spell = message.text[10:]    # remove '/bestiary ' part
        answer = (
            f"{user}, то что ты ищешь находится здесь:\n"
            f"[{spell}](https://dnd.su/articles/bestiary/?search={spell})"
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
            f"{user}, то что ты ищешь находится здесь:\n"
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
