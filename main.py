from aiogram import executor

from bot import dp
from db.db import create_if_not_exist

from handlers import create_char, guide, next_game, start, roll
from utils.masterdata import load_spells

create_if_not_exist()
spell_cards = load_spells()


def register_handlers(dp):
    dp.register_message_handler(start.send_welcome, commands=['start', 'help'])
    dp.register_message_handler(next_game.set_game, commands=['set'])
    dp.register_message_handler(next_game.get_game, commands=['game'])
    dp.register_message_handler(guide.class_list, commands=['class'])
    dp.register_message_handler(guide.spell_search, commands=['spell'])
    dp.register_message_handler(create_char.create_character, commands=['create_character'])
    dp.register_message_handler(create_char.create_character, commands=['create_character'])

    # create_char
    dp.register_callback_query_handler(create_char.reset_char_settings, lambda c: c.data == 'reset_char')
    dp.register_callback_query_handler(create_char.toggle_list, lambda c: c.data == 'toggle_list')
    dp.register_callback_query_handler(create_char.select_class, lambda c: c.data == 'select_class')
    dp.register_callback_query_handler(create_char.selected_class, lambda c: c.data.startswith('selected_class_'))
    dp.register_callback_query_handler(create_char.select_race, lambda c: c.data == 'select_race')
    dp.register_callback_query_handler(create_char.select_race_choice,
                                       lambda c: c.data and c.data.startswith('selected_race_'))
    dp.register_callback_query_handler(create_char.select_story, lambda c: c.data == 'select_story')
    dp.register_callback_query_handler(create_char.select_story_choice,
                                       lambda c: c.data and c.data.startswith('selected_story_'))
    dp.register_callback_query_handler(create_char.select_num_chars, lambda c: c.data == 'select_num_chars')
    dp.register_callback_query_handler(create_char.selected_num_chars,
                                       lambda c: c.data.startswith('selected_num_chars_'))
    dp.register_callback_query_handler(create_char.generate, lambda c: c.data == 'generate')

    dp.register_message_handler(roll.roll_dice_command, commands=['roll'])
    dp.register_message_handler(roll.dice_roll) # should be the last one, because it has a catch-all handler


if __name__ == '__main__':
    register_handlers(dp)
    executor.start_polling(dp, skip_updates=False)
