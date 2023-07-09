import json

import requests
from dataclasses import asdict
from bs4 import BeautifulSoup

from masterdata import SpellCard
# from utils.spells_parser import url

url = 'https://dnd.su/spells/'

# test_case = [
#     SpellCard(title='Адское возмездие', title_en='Hellish rebuke', link='/spells/1-hellish_rebuke/', level='1', school='Воплощение'),
#     SpellCard(title='Антипатия/симпатия', title_en='Antipathy/sympathy', link='/spells/2-antipathy_sympathy/', level='8', school='Очарование'),
#     SpellCard(title='Аура живучести', title_en='Aura of vitality', link='/spells/3-aura_of_vitality/', level='3', school='Воплощение'),
#     SpellCard(title='Аура жизни', title_en='Aura of life', link='/spells/4-aura_of_life/', level='4', school='Ограждение'),
#     SpellCard(title='Аура очищения', title_en='Aura of purity', link='/spells/5-aura_of_purity/', level='4', school='Ограждение'),
#     SpellCard(title='Аура святости', title_en='Holy aura', link='/spells/6-holy_aura/', level='8', school='Ограждение'),
#     SpellCard(title='Безмолвный образ', title_en='Silent image', link='/spells/7-silent_image/', level='1', school='Иллюзия'),
#     SpellCard(title='Бесследное передвижение', title_en='Pass without trace', link='/spells/8-pass_without_trace/', level='2', school='Ограждение'),
#     SpellCard(title='Благословение', title_en='Bless', link='/spells/9-bless/', level='1', school='Очарование'),
#     SpellCard(title='Божественное благоволение', title_en='Divine favor', link='/spells/10-divine_favor/', level='1', school='Воплощение')
# ]
test_case = [
    SpellCard(title='Аура живучести', title_en='Aura of vitality', link='/spells/3-aura_of_vitality/', level='3', school='Воплощение'),
    SpellCard(title='Аура очищения', title_en='Aura of purity', link='/spells/5-aura_of_purity/', level='4', school='Ограждение'),
]

# for card in test_case:
#     card_url = url[:-8] + card.link
#     # card_url = "https://dnd.su/spells/28-magic_mouth/"
#     response = requests.get(card_url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     params_ul = soup.find('ul', class_='params')
#     params_lis = params_ul.find_all('li') if params_ul else []
#
#     for li in params_lis:
#         text = li.get_text(" ", strip=True)
#         if li.get('class') and 'subsection' in li.get('class'):
#             card.description = text
#         elif li.get('class') and 'size-type-alignment' in li.get('class'):
#             card.level_school = text
#         elif ':' in text:
#             detail_name, detail_value = [t.strip() for t in text.split(':', 1)]
#             if detail_name == 'Время накладывания':
#                 card.casting_time = detail_value
#             elif detail_name == 'Дистанция':
#                 card.c_range = detail_value
#             elif detail_name == 'Компоненты':
#                 card.components = detail_value
#             elif detail_name == 'Длительность':
#                 card.duration = detail_value
#             elif detail_name == 'Классы':
#                 card.classes = detail_value
#             elif detail_name == 'Архетипы':
#                 card.archetypes = detail_value
#             elif detail_name == 'Источник':
#                 card.source = detail_value


# # Save to JSON with non-ASCII characters
# with open('spells.json', 'w', encoding='utf-8') as f:
#     json.dump([asdict(card) for card in test_case], f, ensure_ascii=False, indent=4)

# # Load from JSON
# with open('spells.json', 'r', encoding='utf-8') as f:
#     data = json.load(f)
#
# The data object now contains the data loaded from the JSON file
# for card_data in data:
#     card = SpellCard(**card_data)
#
# print(data)


# # Save to JSON
# with open('spells.json', 'w') as f:
#     json.dump([asdict(card) for card in test_case], f)
#
# # Load from JSON
# with open('spells.json', 'r') as f:
#     loaded_data = json.load(f)
#     spell_cards = [SpellCard(**data) for data in loaded_data]
# print(loaded_data)


import json
from masterdata import SpellCard
from dataclasses import asdict

# Load the JSON data
with open('spells.json', 'r', encoding='utf-8') as f:
    spell_data = json.load(f)

# Create dictionary with keys as lowercase title and value as SpellCard instance
spell_dict = {card['title'].lower(): SpellCard(**card) for card in spell_data}

# Save the new data structure back to JSON
with open('spells.json', 'w', encoding='utf-8') as f:
    json.dump({k: asdict(v) for k, v in spell_dict.items()}, f, ensure_ascii=False, indent=4)
