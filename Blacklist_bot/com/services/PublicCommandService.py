from enum import Enum
from com.services import FileService
from com.SafeStr import SafeStr as s


class PublicCommands(Enum):
    CHECK = "!check"


async def process_command(message, channel_name):
    split_message = message.content.split(' ')

    if len(split_message) != 2:
        response_message = ":x: Sorry I accept only 2 parameters but passed "+s.safe_string(len(split_message))+"."
        await message.channel.send(response_message)
        return

    command = split_message[0]
    username = split_message[1]

    if command == PublicCommands.CHECK.value:
        print(s.safe_string(username))
        await message.channel.send('Hello!')
        return
    else:
        response_message = ":x: Unable to resolve command **'" + s.safe_string(command) + "'**. \n\n" \
                           ":green_circle: Available commands in chat **#" + s.safe_string(channel_name) + "** is:\n" \
                           "1) **" + s.safe_string(PublicCommands.CHECK.value) + "** [username]"
        await message.channel.send(response_message)
        return
