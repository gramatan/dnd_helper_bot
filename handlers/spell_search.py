from aiogram import types


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
