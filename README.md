<p align="center">
  <img alt="Static Badge" src="https://img.shields.io/badge/python-3.9_%7C_3.10-blue">
  <img alt="Static Badge" src="https://img.shields.io/badge/bot_version-2.2.1-purple">
  <img alt="GitHub last commit (by committer)" src="https://img.shields.io/github/last-commit/ZiumC/Blacklist_Bot">
</p>   
  
# Blacklist_Bot.py
Bot for discord servers written in Python that allows to keep players in blacklist from any game by using specified commands. To work easily with bot just install <a href="https://github.com/ZiumC/SetChatBox_Addon" rel="nofollow">this</a> addon to the game.

# Features
- Allows to handle messages from server only (private channels aren't handled).
- It have protection against DDOS attacks.
- Generates log to debug (or check) if something went wrong with programme.
- Calls warmane webpage for user data.

# How to run this bot?
1) You should generate your discord token bot (<a href="https://www.writebots.com/discord-bot-token/" rel="nofollow">Tutorial how to do that</a>).  
1.1) After that visit page <a href="https://discord.com/developers/applications" rel="nofollow">Discord Developer Portal</a>.  
1.2) Select your bot and go to **BOT** fold.  
1.3) Search for option ```MESSAGE CONTENT INTENT``` (this is near the end of page) and click on button to enable it (by default this is disabled and it causes an exception in program).  
2) Install docker on your machine. You can use ```docker desktop``` or ```docker command line```. I strongly recommend to use ```docker command line``` (further installation steps will be based on ```docker command line```).
3) Install ```Python 3.9``` or ```Python 3.10``` on your local machine.
4) Setup environment variables ```AdminRole```, ```PublicChanel```, ```ModChanel```, ```GuildID```, ```DiscordToken```, ```ListPath```, ```LogPath```, ```itemDb```, ```enchantDb```
5) Modify file ```config.py```.
```python
import os
from typing import Final

# Better to not modify this
PRIVATE_CHANNEL: Final[str] = 'private'
MAX_DISCORD_MESSAGE_LENGTH: Final[int] = 1999
MAX_REQUEST_PROCESS_TIME: Final[int] = 30
MAX_MODERATION_COMMAND_LENGTH: Final[int] = 2
MAX_PUBLIC_COMMAND_LENGTH: Final[int] = 2
SEPARATOR: Final[str] = "|"
OWNER_ID: Final[str] = os.getenv('OwnerId')

# Strongly recommended is to modify this configuration strings
ADMINISTRATIVE_ROLE: Final[str] = os.getenv('AdminRole')
PUBLIC_CHANNEL_BL: Final[str] = os.getenv('PublicChanel')
MODERATION_CHANNEL_BL: Final[str] = os.getenv('ModChanel')
EXCEPTION_RESPONSE: Final[str] = 'exception'
GUILD_ID: Final[int] = int(os.getenv('GuildID'))
DISCORD_TOKEN: Final[str] = os.getenv('DiscordToken')

# Set paths to bot data files
PATH_TO_BLOCKED_USERS_FILE: Final[str] = os.getenv('ListPath')
PATH_TO_LOG_FILE: Final[str] = os.getenv('LogPath')
PATH_TO_ITEM_DB_FILE: Final[str] = os.getenv('itemDb')
PATH_TO_ENCHANT_TRANSLATION_FILE: Final[str] = os.getenv('enchantDb')

# Config for warmane armory
BASE_ARMORY_URL: Final[str] = "https://armory.warmane.com"
ARMORY_URL: Final[str] = BASE_ARMORY_URL + "/character/"
ARMORY_SERVER: Final[str] = "/Lordaeron/profile"
ARMORY_NOTFOUND_1: Final[str] = "Page not found"
ARMORY_NOTFOUND_2: Final[str] = "does not exist"
ITEM_DATABASE_URL_1: Final[str] = "https://wotlk.cavernoftime.com/item="

# Configs for items
MISSING_FLAG: Final[str] = 'Missing'
DEFAULT_ENCHANT_VALUE: Final[str] = 'None'
DEFAULT_GEMS_VALUE: Final[str] = 'None'
DEFAULT_NOT_EXIST_VALUE: Final[str] = 'Notfound in db'
``` 
5) Add ```Dockerfile``` to project. This file should be placed in ```src``` directory.
```Dockerfile
FROM python:3.10

EXPOSE 443
EXPOSE 80
EXPOSE 53
  
# installing required packages in docker container  
RUN python3 -m pip install -U discord.py  
RUN python3 -m pip install -U requests

# adding bot data to docker container
# note that, clausule copy looks like: COPY [source-local-machine-path] [destination-docker-container-path]
COPY . /srv
  
# running bot  
CMD ["python", "/srv/src/main.py"]  
```
6) Go to ```src``` folder to build docker image. Just type command: ```docker build --network=host -t [your-image-name] . ```
7) Create file ```docker-compose.yml``` as follow:
```yaml
version: '3.8'
services:
  [your-service-name]:
    image: '[your-image-name]'
    restart: 'unless-stopped'
    container_name: '[your-container-name]'
    network_mode: 'host' #<- I know this is unelegant but without that appears problem:
                         #'Temporary failure in name resolution [Errno -3] ... unable connect to discord.com:443'
    volumes:
      - './Bot-Data:/srv/Bot-Data'    
    environment:
      - OwnerId=[your id]
      - AdminRole=[admin role]
      - PublicChanel=[pub channel]
      - GuildID=[your discord server id]
      - DiscordToken=[your discord token]
      - ListPath=/srv/Bot-Data/bl.csv
      - LogPath=/srv/Bot-Data/log.txt
      - itemDb=/srv/Bot-Data/itemsDB.csv
      - enchantDb=/srv/Bot-Data/itemId-to-enchantId.txt
    mem_reservation: "1g"
    cpus: "1"
    cpuset: "2" 
```
8) To run just type ```docker-compose up -d```
  

# How to work with bot?  
To run that bot on your discord server you should create 2 separate channels. First (public) channel will be accessible for everyone without any special role. Second channel (administrative) will be accessible for only users who had a **special administrative role**. That special role prevents untrusted users to perform actions such as adding, modifying or deleting users on blacklist.

1) Public channel commands:
- ```!help``` - just prints available commands in public channel.
- ```!check [username_to_check]``` - checks if passed username exist on blacklist. 
2) Administrative channel commands:
- ```!help``` - just prints available commands in moderation channel.
- ```!add [username_to_add] -[reason why player is added]``` - adds player with reason to blacklist.
- ```!modify [username_to_update] -[updated reason why player exist on blacklist]``` - updates player and reason why still exist in blacklist.
- ```!delete [username_to_delete]``` - removes player from blacklist.
- ```!last``` - prints last added player to blacklist.
- ```!log_err [type] (type can be: CRITICAL, ERROR, WARNING)``` - returns bot log
- ```!clear_log (viable for creator)``` - clears bot log
- ```$Some message``` - bot will ignore message that starts with **$**. This is used to announce some changes or inform other moderative users that bot will be e.g. turned off, updated, etc.,  
    
# Packages used
- discord.py (2.3.0)
- os
- re
- logging
- date
- datetime
- Enum
- Final


# Links
- <a href="https://discordpy.readthedocs.io/en/latest/api.html" rel="nofollow">Discord API documentation</a>
- <a href="https://www.writebots.com/discord-bot-token" rel="nofollow">Tutorial how to generate a discord bot token</a>
- <a href="https://discordgsm.com/guide/how-to-get-a-discord-bot-token" rel="nofollow"> Other tutorial how to generate a discord bot token</a>
