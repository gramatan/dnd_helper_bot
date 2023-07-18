from aiogram import types

from bot import dp

HELP_MESSAGE = (
    "Привет! Я бот, который может помочь в ваших DnD приключениях, бросая кости за вас и предоставляя информацию "
    "из различных справочников. Вот, что я могу сделать:\n\n"

    "🎲 Бросить кубик: отправьте сообщение в формате 'NdM+K', где N - количество кубиков, "
    "M - количество граней на кубике, K - модификатор (необязательно). Например, '2d20+5'. "
    "Я вычислю результат для вас!\n\n"

    "🎲 Бросить один кубик: используйте команду /roll N, где N - количество сторон на кубике "
    "(по умолчанию 20, если N не указано). Например, '/roll 100' бросит 100-гранный кубик за вас.\n\n"

    "📅 Установить информацию о следующей игре: используйте команду /set, "
    "а потом получить ее обратно с помощью команды /game.\n\n"

    "📚 Поиск заклинаний: используйте команду /spell 'Название заклинания'. "
    "Если заклинание есть в моей базе, я предоставлю информацию о нем, иначе я помогу вам его найти.\n\n"

    "📚 Поиск механик: используйте команду /mech 'Название механики'.\n\n"

    "📚 Поиск предметов: используйте команду /item 'Название предмета'.\n\n"

    "📚 Поиск по бестиарию: используйте команду /bestiary 'Название существа'.\n\n"

    "📚 Поиск по классам: используйте команду /class 'Название класса'.\n\n"

    "📚 Поиск черт: используйте команду /feat 'Название черты'. "
    "Если черта есть в моей базе, я предоставлю информацию о ней, иначе я помогу вам с её поиском.\n\n"

    "📝 Создать случайного персонажа: используйте команду /create\\_character. "
    "Вы можете выбирать класс, расу, предысторию и количество персонажей.\n\n"

    "Вот список сайтов, которые могут помочь:\n"
    "[DnD.su. Справочник по заклинаниям](https://dnd.su/spells)\n"  
    "[DnD.su. Справочник по классам](https://dnd.su/class)\n"
    "[DnD.su. Справочник по расам](https://dnd.su/race)\n\n"
    "[Интерактивный чарлист](https://longstoryshort.app/characters/list)\n\n"
    "[Правила для начинающих игроков](https://www.dungeonsanddragons.ru/bookfull/5ed/5e%20starter%20set%20-%20basic%20rules%20RUS.pdf)\n"
    "[Миниатюры персонажей Hero Forge](https://www.heroforge.com)\n"
)

START_MESSAGE = (
    "Привет! Я бот, который может помочь в ваших DnD приключениях.\n"
    "Вы можете использовать команду /help чтобы узнать больше обо мне и моих возможностях."
)


async def start_message(message: types.Message):
    welcome_message = START_MESSAGE
    await message.reply(welcome_message, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)


async def help_message(message: types.Message):
    welcome_message = HELP_MESSAGE
    await message.reply(welcome_message, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)
