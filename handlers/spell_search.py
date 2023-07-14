from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def spell_search(message: types.Message):
    from main import spell_cards, logger
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
        logger.debug(f"matches: {matches}")
        if len(matches) == 1:
            card = spell_cards[matches[0]]
            details = {
                "Время накладывания": card.casting_time,
                "Дистанция": card.c_range,
                "Компоненты": card.components,
                "Длительность": card.duration,
                "Классы": card.classes,
                "Архетипы": card.archetypes,
            }

            details_text = "\n".join([f"{key}: {value}" for key, value in details.items() if value is not None])

            answer = f"{card.title} [{card.title_en}]\n\n" \
                     f"{card.level_school}\n" \
                     f"{details_text}\n\n" \
                     f"{card.description}\n\n" \
                     f"[Ссылка на DnD.su](https://dnd.su{card.link})"

            await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)
        elif 1 < len(matches) < 9:
            inline_kb_full = InlineKeyboardMarkup(row_width=2)
            buttons_list = [InlineKeyboardButton(str(i+1), callback_data=f"spell_{matches[i]}") for i in range(len(matches))]
            inline_kb_full.add(*buttons_list)

            spells_text = '\n'.join([f"{i+1}. {spell}" for i, spell in enumerate(matches)])
            await message.reply(f"В базе несколько заклинаний по вашему запросу:\n{spells_text}", reply_markup=inline_kb_full)

        else:
            answer = (
                "твоё заклинание где-то здесь:\n"
                f"[{spell}](https://dnd.su/spells/?search={spell})"
            )
            await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)


async def spell_callback_query(call: types.CallbackQuery):
    from main import spell_cards
    from bot import bot

    if call.data.startswith('spell_'):
        spell = call.data[6:]
        card = spell_cards[spell]

        details = {
            "Время накладывания": card.casting_time,
            "Дистанция": card.c_range,
            "Компоненты": card.components,
            "Длительность": card.duration,
            "Классы": card.classes,
            "Архетипы": card.archetypes,
        }

        details_text = "\n".join([f"{key}: {value}" for key, value in details.items() if value is not None])

        answer = f"{card.title} [{card.title_en}]\n\n" \
                 f"{card.level_school}\n" \
                 f"{details_text}\n\n" \
                 f"{card.description}\n\n" \
                 f"[Ссылка на DnD.su](https://dnd.su{card.link})"

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer)
