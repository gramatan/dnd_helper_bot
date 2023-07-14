from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def generate_feat_card_details(card):
    if card.prerequisites:
        details = {
            "Требования": card.prerequisites,
            "Полное описание": card.description,
        }
    else:
        details = {
            "Полное описание": card.description,
        }

    details_text = "\n".join([f"{key}: {value}" for key, value in details.items() if value is not None])

    return f"{card.title} [{card.title_en}]\n\n" \
           f"{details_text}\n\n" \
           f"[Ссылка на DnD.su](https://dnd.su{card.link})"


async def feat_search(message: types.Message):
    from main import feat_cards, logger
    user = message.from_user.first_name
    if len(message.text) < 6:
        await message.reply(
            f"{user}, ты забыл ввести слова для поиска после /feat\n"
            "например:\n"
            "/feat Ударный щит\n"
            "/feat Меткий выстрел"
        )
    else:
        feat = message.text[6:]    # remove '/feat ' part
        feat_lower = feat.lower()
        matches = [key for key in feat_cards.keys() if feat_lower in key]
        logger.debug(f"matches: {matches}")
        if len(matches) == 1:
            card = feat_cards[matches[0]]
            answer = await generate_feat_card_details(card)
            await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)

        elif 1 < len(matches) < 9:
            inline_kb_full = InlineKeyboardMarkup(row_width=6)
            buttons_list = [InlineKeyboardButton(str(i+1),
                                                 callback_data=f"feat_{matches[i]}") for i in range(len(matches))]
            inline_kb_full.add(*buttons_list)

            feats_text = '\n'.join([f"{i+1}. {feat_cards[feat].title}"
                                    f" [{feat_cards[feat].title_en}]" for i, feat in enumerate(matches)])
            await message.reply(f"В базе несколько особенностей по вашему запросу:\n{feats_text}",
                                reply_markup=inline_kb_full)

        else:
            answer = (
                "твоя особенность где-то здесь:\n"
                f"[{feat}](https://dnd.su/feats/?search={feat})"
            )
            await message.reply(answer, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)


async def feat_callback_query(call: types.CallbackQuery):
    from main import feat_cards
    from bot import bot

    if call.data.startswith('feat_'):
        feat = call.data[5:]
        card = feat_cards[feat]
        answer = await generate_feat_card_details(card)

        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer)
