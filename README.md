<p align="center">
  <img alt="Static Badge" src="https://img.shields.io/badge/python-3.9_%7C_3.10-blue">
  <img alt="Static Badge" src="https://img.shields.io/badge/bot_version-1.5-purple">
  <img alt="GitHub last commit (by committer)" src="https://img.shields.io/github/last-commit/ZiumC/Blacklist_Bot">
</p>   
  
# Blacklist_Bot.py
Bot for discord servers written in Python that allows to keep players in blacklist from any game by using specified commands. 

# Features
- This project is using ```async``` and ```await``` methods to call Discord API.
- Allows to handle messages from server only (private channels aren't handled).
- It have protection against DDOS attacks.
- Generates log to debug (or check) if something went wrong with programme.

# How to run this bot?
1) You should generate your discord token bot (<a href="https://www.writebots.com/discord-bot-token/" rel="nofollow">Tutorial how to do that</a>).  
1.1) After that visit page <a href="https://discord.com/developers/applications" rel="nofollow">Discord Developer Portal</a>.  
1.2) Select your bot and go to **BOT** fold.  
1.3) Search for option ```MESSAGE CONTENT INTENT``` (this is near the end of page) and click on button to enable it (by default this is disabled and it causes an exception in program).  
2) Install docker on your machine. You can use ```docker desktop``` or ```docker command line```. I strongly recommend to use ```docker command line``` (further installation steps will be based on ```docker command line```).
3) Install ```Python 3.9``` or ```Python 3.10``` on your local machine.
4) Modify file ```config.py```.
```python
import os
from typing import Final

# Better to not modify this
PRIVATE_CHANNEL: Final[str] = 'private'
MAX_DISCORD_MESSAGE_LENGTH: Final[int] = 1999
MAX_REQUEST_PROCESS_TIME: Final[int] = 30
MAX_MODERATION_COMMAND_LENGTH: Final[int] = 2
MAX_PUBLIC_COMMAND_LENGTH: Final[int] = 2

# Strongly recommended is to modify this configuration strings
# Administrative channel name that will be accessible for users who have proper permissions to modify blacklist
ADMINISTRATIVE_ROLE: Final[str] = ''
# Public channel name that will be accessible for all users to check if someone exist in blacklist
PUBLIC_CHANNEL_BL: Final[str] = ''
# Administrative channel name that will be accessible for users who have proper permissions to modify blacklist
MODERATION_CHANNEL_BL: Final[str] = ''
# Your awesome exception message goes here
EXCEPTION_RESPONSE: Final[str] = ''
# Your server id goes here - this is used to prevent use your bot with your token on other discord server
GUILD_ID: Final[int] = 0
# Your discord token goes here
DISCORD_TOKEN: Final[str] = ''

# Set path to blacklist file. Note that, path should contain file name with extension (recommended file extension is .csv)
PATH_TO_BLOCKED_USERS_FILE: Final[str] = ''
# Set path to blacklist log. Note that, path should contain file name with extension (recommended file extension is .txt)
PATH_TO_LOG_FILE: Final[str] = ''
``` 
5) Add ```Dockerfile``` to project. This file should be placed in ```src``` directory.
```Dockerfile
FROM python:3.10  
# creating directories for project in docker container  
RUN mkdir -p /srv/src  
RUN mkdir -p /srv/src/services  
RUN mkdir -p /srv/bot-data  
RUN mkdir -p /srv/bot-data/blacklist  
RUN mkdir -p /srv/bot-data/log
  
# installing required packages in docker container  
RUN python3 -m pip install -U discord.py  
  
# adding bot data to docker container
# note that, clausule copy looks like: COPY [source-local-machine-path] [destination-docker-container-path]
COPY ./Bot-Data/bl.csv /srv/bot-data/blacklist/bl.csv  
COPY ./Bot-Data/log.txt /srv/bot-data/log/log.txt  
  
# adding project files from local machine to docker container
# note that, clausule add looks like: ADD [source-local-machine-path] [destination-docker-container-path]  
ADD main.py /srv/src  
ADD safe_str.py /srv/src  
ADD message_handler.py /srv/src  
ADD config.py /srv/src 
ADD ./services/admin_service.py /srv/src/services  
ADD ./services/file_service.py /srv/src/services  
ADD ./services/public_command_service.py /srv/src/services  
  
# running bot  
CMD ["python", "/srv/src/main.py"]  
```
6) (OPTIONAL) You can limit resources used by docker container. To do that just add ```Docker-compose.yml``` to project. This file should be placed in ```src``` directory.
```yml
version: "3.9"
service:
  bot-service:
    image: [your-awesome-image-name]
    container_name: [your-awesome-container-name]
    mem_reservation: "1g"
    cpus: "1"
    cpuset: "2"
```
7) Build your image and run the container. To do thad just follow these steps:    
1. Go to ```src``` folder of project: ```cd "/path/to/bot/project/on/local-machine/src"```    
2. Build your image: ```docker build -t [your-awesome-image-name] . ```    
3. Run your docker container with image: ```ocker run --name [your-awesome-container-name] [your-awesome-image-name]```    

# Troubleshooting with module names - python
If your bot can't run due to exception ```No module named 'src'``` or ```Package doesn't have process_command(...)``` you have to modify imports of local packages - just add ```src.```.   
Just change imports in entire bot project files from this:
```python
# Procject file: main.py
import discord
import logging
from discord.ext import commands
import config as conf
import services.admin_service as adm
import services.public_command_service as pub
from message_handler import Handler as messHandler
from safe_str import SafeStr as sStr

# Procject file: admin_service.py
import logging
import re as regex
from enum import Enum
import config as conf
from services import file_service
from safe_str import SafeStr as sStr
from message_handler import Handler as messHandler

# Procject file: file_service.py
import os
import logging
from datetime import date
from datetime import datetime
import config as conf
from safe_str import SafeStr as sStr

# Procject file: public_command_service.py
import logging
from enum import Enum
import config as conf
from services import file_service
from safe_str import SafeStr as sStr
from message_handler import Handler as messHandler
```
to this:
```python
# Procject file: main.py
import discord
import logging
from discord.ext import commands
import src.config as conf
import src.services.admin_service as adm
import src.services.public_command_service as pub
from src.message_handler import Handler as messHandler
from src.safe_str import SafeStr as sStr

# Procject file: admin_service.py
import logging
import re as regex
from enum import Enum
import src.config as conf
from src.services import file_service
from src.safe_str import SafeStr as sStr
from src.message_handler import Handler as messHandler

# Procject file: file_service.py
import os
import logging
from datetime import date
from datetime import datetime
import src.config as conf
from src.safe_str import SafeStr as sStr

# Procject file: public_command_service.py
import logging
from enum import Enum
import src.config as conf
from src.services import file_service
from src.safe_str import SafeStr as sStr
from src.message_handler import Handler as messHandler
```  
# Troubleshooting with temporary failure in name resolution [Errno -3]
If you are running docker on linux machine, you may meet problem: 'temporary failure in name resolution' on bot startup. It may aquire because linux machine by default uses local DNS server delivered by your Internet operator. So if you connect to server discord.com every day, probably you won't see this problem. But if your local DNS doesn't cache current IP of discord.com, bot will stop working. To solve this problem you should follow these steps:
1) Run command: ```sudo nano /etc/default/docker```
2) Inside this file add line: ```DOCKER_OPTS="--dns 8.8.8.8 --dns 10.252.252.252"``` then save it
3) Run command: ```docker restart```
4) At the end run docker container

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
