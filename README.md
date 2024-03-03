# DnD Helper Bot

DnD Helper is a Telegram bot designed to assist with your Dungeons & Dragons gaming sessions. It can roll dice, set and retrieve game information, and provide spell descriptions, among other features.
Try it here:

![img_1.png](img_1.png)


## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Deployment](#deployment)
- [Updating the Bot](#updating-the-bot)
- [Moving the Container](#moving-the-container)

## Features

- **Random character creation**: Use the `/create_character` command, follow the prompted button setup, and generate your character.
- **Dice rolling**: The bot can roll a dice with a specified number of sides. Use the command `/roll N`, where N is the number of sides on the dice (defaults to 20 if not specified).
- **Roll stats for character creation**: Generates character stats by rolling 4d6 dice for each stat, discarding the lowest die each time. Use `/roll_stats` or `/roll_stats N` for N sets of rolls, choosing the set with the highest sum.
- **Advanced dice rolling**: Use the format `NdM+K`, where N is the number of dice, M is the number of sides per dice, and K is an optional modifier.
- **Game scheduling**: Use `/set` followed by your text to save information about your next game. Use `/game` to retrieve this information.
- **Information lookup**: Use `/spell`, `/class`, `/item`, `/bestiary`, `/feat` and `/mech` commands followed by their respective search term to get relevant information. If the item is found in the bot's database, it will provide a detailed description; otherwise, it will return a link to the DnD resource for further searching.

## Prerequisites

- Python 3.9 or higher
- Docker
- A bot token from BotFather on Telegram

## Setup

1) Clone this repository to your local machine.
2) Navigate into the cloned repository.
3) Set up a virtual environment and activate it.
4) Install the necessary dependencies using `pip install -r requirements.txt`.
5) Replace the placeholder token in config.py with your own bot token.
6) Run the data scraping script using `python utils/spells_scraper.py` and `python utils/feats_scraper.py`. This will populate your spells.json and feats files. You don't need to do this every time. Just use the file provided.
7) Run the bot using `python main.py`.


## Deployment

To deploy the application using Docker Compose:

1. Clone the repository and navigate to its directory.
2. Run the application using Docker Compose:

   ```bash
   docker build -t my_dnd_bot:0.5.0 .
   docker-compose up -d
   ```
   
---

There's nothing to see here.
For BotFather:
start - Начать использование бота и узнать о его функциях
help - Получить информацию о том, как использовать бота
roll - Бросить кубики. Используйте формат /NdM+K
roll_stats - Бросить кубики для определения стартовых характеристик персонажа
set - Установить расписание следующей игры
game - Получить расписание следующей игры
spell - Найти или получить описание заклинания, например, /spell Fireball
feat - Найти или получить описание черты, например, /feat Лекарь
mech - Найти механику, например, /mech 'Sneak Attack'
item - Найти предмет, например, /item 'Longsword'
bestiary - Найти существо в бестиарии, например, /bestiary 'Dragon'
class - Список ссылок на классы
create_character - Создать случайного персонажа DnD. Позволяет выбрать пресет, класс, расу, предысторию и количество персонажей для создания.
