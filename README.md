# DnD Helper Bot

DnD Helper is a Telegram bot designed to assist with your Dungeons & Dragons gaming sessions. It can roll dice, set and retrieve game information, and provide spell descriptions, among other features.
Try it here:
![IMG_20230717_171553_992~01](https://github.com/gramatan/dnd_helper_bot/assets/78417563/feeb8ff7-1ac1-443e-92f4-e15084a7bbc8)


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

1) Build a Docker image using `docker build -t my_dnd_bot .`.
2) Create Volume to keep your database safe using `docker volume create my_dnd_bot_db`.
3) Run a Docker container from the image using `docker run -v my_dnd_bot_db:/app/db -d --restart unless-stopped my_dnd_bot`.

## Updating the Bot

1) Make changes to your source files.
2) If changes were made to the data scraping script, run it again with `python utils/spells_scraper.py` to update your spells.json file.
3) Rebuild the Docker image with `docker build --no-cache -t my_dnd_bot .`.
4) Stop and remove the old container using `docker rm -f <container_id>`.
5) Run a new container from the updated image.

## Moving the Container

### Saving a Docker Image to a .tar file

After you've built your Docker image:

1) Use the `docker save` command followed by the `-o` flag, the name of your output .tar file, and the name of your image. 

For example, if your image is named "my_dnd_bot", the command would look like this:

```bash
docker save -o my_dnd_bot.tar my_dnd_bot
```

### Loading a Docker Image from a .tar file

On the machine where you want to load the Docker image:

1) Transfer the .tar file to this machine using any method you prefer (e.g., SCP, SFTP, USB drive).
2) Use the `docker load` command followed by `-i` flag and the name of your .tar file.

For example:

```bash
docker load -i my_dnd_bot.tar
```

After this, you can use `docker run` to start a container from the image, just as you would if you had built the image on that machine.

---

There's nothing to see here.
For BotFather:
start - Начать использование бота и узнать о его функциях
help - Получить информацию о том, как использовать бота
roll - Бросить кубики. Используйте формат /NdM+K
set - Установить расписание следующей игры
game - Получить расписание следующей игры
spell - Найти или получить описание заклинания, например, /spell Fireball
feat - Найти или получить описание черты, например, /feat Лекарь
mech - Найти механику, например, /mech 'Sneak Attack'
item - Найти предмет, например, /item 'Longsword'
bestiary - Найти существо в бестиарии, например, /bestiary 'Dragon'
class - Список ссылок на классы
create_character - Создать случайного персонажа DnD. Позволяет выбрать пресет, класс, расу, предысторию и количество персонажей для создания.
