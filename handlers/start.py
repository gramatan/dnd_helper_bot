from aiogram import types

from bot import dp

WELCOME = (
        "Привет! Я бот, который может помочь в ваших DnD приключениях, бросая кости за вас. "
        "Просто отправьте сообщение в формате '/NdM+K', где N - количество кубиков, "
        "M - количество граней на кубике, K - модификатор (необязательно). Например, '/2d20+5'. "
        "Я вычислю результат для вас!\n\n"
        "Вы также можете использовать команду /roll N, где N - это количество сторон на кубике "
        "(по умолчанию 20, если N не указано). "
        "Это простой способ быстро бросить один кубик. Например, '/roll 100' бросит 100-гранный кубик за вас.\n\n"
        "Вы также можете установить информацию о следующей игре с помощью команды /set, "
        "а потом получить ее обратно с помощью команды /game.\n\n"
        "Если вы хотите найти описание заклинания, просто используйте команду /spell 'Название заклинания'. "
        "Для поиска по справочнику классов, используйте команду /class 'Название класса'.\n\n"
        "Используйте команду /create\\_character для создания случайных персонажей. "
        "Вы можете выбирать класс, расу, предысторию и количество персонажей.\n\n"
        "Вот список сайтов, которые могут помочь:\n"
        "[DnD.su. Справочник по заклинаниям](https://dnd.su/spells)\n"  
        "[DnD.su. Справочник по классам](https://dnd.su/class)\n"
        "[DnD.su. Справочник по расам](https://dnd.su/race)\n\n"
        "[Интерактивный чарлист](https://longstoryshort.app/characters/list)\n\n"
        "[Правила для начинающих игроков](https://www.dungeonsanddragons.ru/bookfull/5ed/5e%20starter%20set%20-%20basic%20rules%20RUS.pdf)\n"
        "[Миниатюры персонажей Hero Forge](https://www.heroforge.com)\n"
    )


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    welcome_message = WELCOME
    await message.reply(welcome_message, parse_mode=types.ParseMode.MARKDOWN, disable_web_page_preview=True)
