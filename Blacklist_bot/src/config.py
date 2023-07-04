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

# Strongly recommended is that to use system environment
PATH_TO_BLOCKED_USERS_FILE: Final[str] = os.getenv('PATH_TO_BLOCKED_USERS_FILE')
PATH_TO_LOG_FILE: Final[str] = os.getenv('PATH_TO_LOG_FILE')
