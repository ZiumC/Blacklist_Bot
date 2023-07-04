<p align="center"><img alt="Static Badge" src="https://img.shields.io/badge/python-3.9-blue"> <img alt="Static Badge" src="https://img.shields.io/badge/bot_version-1.0-green"></p>   
  
# Blacklist_Bot.py
Bot for discord servers written in Python that allows to keep players in black list from any game by using specified commands. 

# Features
- This project is using ```async ``` and ```await``` methods to call Discord API.
- Allows to handle messages from server only (private channels aren't handled).
- It have protection against DDOS attacks.
- Generates log to debug (or check) if something went wrong with programme.

# How to install this bot?
1) Firstly you should generate your discord token bot (<a href="https://www.writebots.com/discord-bot-token/" rel="nofollow">Tutorial how to do that</a>). 
2) Secondly you should have had installed ```Python 3.9```.
3) Thirdly add to your system enviroment variables for ```PATH_TO_BLOCKED_USERS_FILE```, ```PATH_TO_LOG_FILE``` and ```DiscordToken```.  

```text
Windows users:
1) Launch "Control Panel".  
2) "System and Security".  
3) Select "System".  
4) On the rightside search for "Advanced system settings" then click on it.  
5) Switch to "Advanced" tab.  
6) Click on "Environment variables".  
7) Choose "User variables for [username]".  
8) Choose "New".  
9) Enter the variable "Name" and "Value"

Linux users (just type in terminal):
1) export PATH_TO_BLOCKED_USERS_FILE="path/to/blacklist/file.csv"
2) export PATH_TO_LOG_FILE="path/to/log/file.txt"
3) export DiscordToken="your-amazing-discord-token"
```    
4) Fourthly you should modify ```config.py``` file.
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
# Administrative role name in discord server
ADMINISTRATIVE_ROLE: Final[str] = ''
# Public channel name that will be accessible for all users to check if someone exist in blacklist
PUBLIC_CHANNEL_BL: Final[str] = ''
# Administrative channel name that will be accessible for users who have proper permissions to modify blacklist
MODERATION_CHANNEL_BL: Final[str] = ''

# Strongly recommended is that to use system environment
# Set path to blacklist file. Note that, path should contain file name with extension (recommended file extension is .csv)
PATH_TO_BLOCKED_USERS_FILE: Final[str] = os.getenv('PATH_TO_BLOCKED_USERS_FILE')
# Set path to blacklist log. Note that, path should contain file name with extension (recommended file extension is .txt)
PATH_TO_LOG_FILE: Final[str] = os.getenv('PATH_TO_LOG_FILE')
```
5) Last thing is just running file ```main.py```.

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
