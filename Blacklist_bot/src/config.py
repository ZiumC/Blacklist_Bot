import os
from typing import Final

PRIVATE_CHANNEL: Final[str] = 'private'
ADMINISTRATIVE_ROLE: Final[str] = 'nowa rola'
PUBLIC_CHANNEL_BL: Final[str] = 'ogólny'
MODERATION_CHANNEL_BL: Final[str] = 'moderacja'
MAX_MESSAGE_LENGTH: Final[int] = 1999
MAX_PROCESS_TIME: Final[int] = 30

PATH_TO_BLOCKED_USERS_FILE: Final[str] = os.getenv('PATH_TO_BLOCKED_USERS_FILE')
PATH_TO_LOG_FILE: Final[str] = os.getenv('PATH_TO_LOG_FILE')
