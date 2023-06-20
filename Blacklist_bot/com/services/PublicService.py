from enum import Enum
from com.services import FileService


class PublicCommands(Enum):
    CHECK = "!check"


async def process_command(message, channel_name):
    split_message = message.content.split(' ')

    if len(split_message) != 2:
        response_message = ":x: Sorry I accept only 2 parameters but passed {}. \n\n"
        await message.channel.send(response_message.format(len(split_message)))
        return

    command = split_message[0]
    username = split_message[1]

    if command == PublicCommands.CHECK.value:
        await message.channel.send('Hello!')
        return
    else:
        response_message = ":x: Unable to resolve command **'{}'**. \n\n" \
                           ":green_circle: Available commands in chat **#{}** is:\n" \
                           "1) **!check** [username]"
        await message.channel.send(response_message.format(command, channel_name))
        return
