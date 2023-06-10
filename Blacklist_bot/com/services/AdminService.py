from enum import Enum
from com import MessageHandler

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
    username = split_message[1]

    if command == AdminCommands.ADD.value:
        if not await handler.is_message_length_valid(message, split_message, COMMAND_LENGTH_3):
            return

        description_reason = split_message[2]
        await message.channel.send('Add new person')
        return
    
    elif command == AdminCommands.MODIFY.value:
        if not await handler.is_message_length_valid(message, split_message, COMMAND_LENGTH_3):
            return

        description_reason = split_message[2]
        await message.channel.send('Modify person')
        return

    elif command == AdminCommands.DELETE.value:
        if not await handler.is_message_length_valid(message, split_message, COMMAND_LENGTH_2):
            return

        await message.channel.send('Delete person')
        return

    else:
        response_message = ":x: Unable to resolve command **'{}'**. \n\n" \
                           ":green_circle: Available commands in chat **#{}** is:\n" \
                           "1) **{}** [username] [description]\n" \
                           "2) **{}** [username] [description]\n" \
                           "3) **{}** [username]"
        await message.channel.send(response_message.format(command,
                                                           channel_name,
                                                           AdminCommands.ADD.value,
                                                           AdminCommands.MODIFY.value,
                                                           AdminCommands.DELETE.value))
        return
