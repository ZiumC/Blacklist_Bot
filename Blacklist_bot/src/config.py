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
