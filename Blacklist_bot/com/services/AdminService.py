from enum import Enum
from com import MessageHandler
from com.services import FileService
import com.SafeStr as m

COMMAND_LENGTH_3 = 3
COMMAND_LENGTH_2 = 2


class AdminCommands(Enum):
    ADD = '!add'
    MODIFY = '!modify'
    DELETE = '!delete'


async def process_command(message, channel_name):
    handler = MessageHandler.Handler

    split_message = message.content.split(' ')
    command = split_message[0]

    if command == AdminCommands.ADD.value:
        if not await handler.is_message_length_valid(message, split_message, COMMAND_LENGTH_3):
            return
        username = split_message[1]
        description_reason = split_message[2]
        # FileService.add_user_to_bl(username, description_reason)
        await message.channel.send('Add new person')
        return

    elif command == AdminCommands.MODIFY.value:
        if not await handler.is_message_length_valid(message, split_message, COMMAND_LENGTH_3):
            return
        username = split_message[1]
        description_reason = split_message[2]
        await message.channel.send('Modify person')
        return

    elif command == AdminCommands.DELETE.value:
        if not await handler.is_message_length_valid(message, split_message, COMMAND_LENGTH_2):
            return

        await message.channel.send('Delete person')
        return

    else:
        response_message = ":x: Unable to resolve command **'" + m.SafeStr.safe_string(command) + "'**. \n\n" \
                           ":green_circle: Available commands in chat **#" + m.SafeStr.safe_string(channel_name) + "** is:\n" \
                           "1) **" + m.SafeStr.safe_string(AdminCommands.ADD.value) + "** [username] [description]\n" \
                           "2) **" + m.SafeStr.safe_string(AdminCommands.MODIFY.value) + "** [username] [description]\n" \
                           "3) **" + m.SafeStr.safe_string(AdminCommands.DELETE.value) + "** [username]"
        await message.channel.send(response_message)
        return
