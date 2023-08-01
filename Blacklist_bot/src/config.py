import os
from typing import Final

# Better to not modify this
PRIVATE_CHANNEL: Final[str] = 'private'
MAX_DISCORD_MESSAGE_LENGTH: Final[int] = 1999
MAX_REQUEST_PROCESS_TIME: Final[int] = 30
MAX_MODERATION_COMMAND_LENGTH: Final[int] = 2
MAX_PUBLIC_COMMAND_LENGTH: Final[int] = 2

# Strongly recommended is to modify this configuration strings
ADMINISTRATIVE_ROLE: Final[str] = ''
PUBLIC_CHANNEL_BL: Final[str] = ''
MODERATION_CHANNEL_BL: Final[str] = ''
EXCEPTION_RESPONSE: Final[str] = ''
GUILD_ID: Final[int] = 0
DISCORD_TOKEN: Final[str] = ''

# Set paths to bod data files
PATH_TO_BLOCKED_USERS_FILE: Final[str] = ''
PATH_TO_LOG_FILE: Final[str] = ''
