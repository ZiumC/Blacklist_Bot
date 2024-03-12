import os
from typing import Final

# Better to not modify this
PRIVATE_CHANNEL: Final[str] = 'private'
MAX_DISCORD_MESSAGE_LENGTH: Final[int] = 1999
MAX_REQUEST_PROCESS_TIME: Final[int] = 30
MAX_MODERATION_COMMAND_LENGTH: Final[int] = 2
MAX_PUBLIC_COMMAND_LENGTH: Final[int] = 2
SEPARATOR: Final[str] = "|"

# Strongly recommended is to modify this configuration strings
ADMINISTRATIVE_ROLE: Final[str] = os.getenv('AdminRole')
PUBLIC_CHANNEL_BL: Final[str] = os.getenv('PublicChanel')
MODERATION_CHANNEL_BL: Final[str] = os.getenv('ModChanel')
EXCEPTION_RESPONSE: Final[str] = 'exception'
GUILD_ID: Final[int] = int(os.getenv('GuildID'))
DISCORD_TOKEN: Final[str] = os.getenv('DiscordToken')

# Set paths to bod data files
PATH_TO_BLOCKED_USERS_FILE: Final[str] = os.getenv('ListPath')
PATH_TO_LOG_FILE: Final[str] = os.getenv('LogPath')

ARMORY_URL: Final[str] = "https://armory.warmane.com/character/"
ARMORY_SERVER: Final[str] = "/Lordaeron/profile"
ARMORY_NOTFOUND_1: Final[str] = "Page not found"
ARMORY_NOTFOUND_2: Final[str] = "does not exist"
ITEM_DATABASE_URL: Final[str] = "https://wotlk.cavernoftime.com/item="


