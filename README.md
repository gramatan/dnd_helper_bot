# DnD Helper Bot

DnD Helper is a Telegram bot designed to assist with your Dungeons & Dragons gaming sessions. It can roll dice for you, set and recall game information, and provide spell information.
Features

* Random character creation tool. Use /create_character setup it with buttons and press generate.
* Dice rolling: The bot can roll dice with a specified number of sides. Use the command /roll N, where N is the number of sides on the dice (default 20).
* Advanced dice rolling: Use the format /NdM+K, where N is the number of dice, M is the number of sides per dice, and K is an optional modifier.
* Game information: Use /set followed by your text to save information about your next game. Use /game to retrieve this information.
* Spell lookup: Use /spell followed by the spell name to get a link to the spell's description.

##  Prerequisites

    Python 3.9 or higher
    Docker
    A bot token from BotFather on Telegram

##  Setup

1) Clone this repository to your local machine.
2) Navigate into the cloned repository.
3) Set up a virtual environment and activate it.
4) Install the necessary dependencies using pip install -r requirements.txt.
5) Replace the placeholder token in config.py with your own bot token.
6) Run the bot using python main.py.

##  Deployment

7) Build a Docker image using `docker build -t my_dnd_bot .`.
8) Run a Docker container from the image using `docker run -d --restart unless-stopped my_dnd_bot`.

##  To update the bot:

9) Make changes to your source files.
10) Rebuild the Docker image with `docker build --no-cache -t my_dnd_bot .`.
11) Stop and remove the old container using `docker rm -f <container_id>`.
12) Run a new container from the updated image.
