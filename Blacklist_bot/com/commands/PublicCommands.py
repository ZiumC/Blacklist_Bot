from enum import Enum


class PublicCommands(Enum):
    CHECK = "!check"


async def process_command(message, channel):
    split_message = message.content.split(' ')

    if len(split_message) != 2:
        response_message = "Sorry, but I accept only 2 parameters."
        await message.channel.send(response_message)
        return

    command = split_message[0].replace("\\s", "")
    username = split_message[1].replace("\\s", "")

    if command == PublicCommands.CHECK.value:
        await message.channel.send('Hello!')
        return
    else:
        response_message = ":x: Unable to resolve command **'{}'**. \n\n" \
                           ":green_circle: Available commands in chat **#{}** is:\n" \
                           "1) **!check** [username]"
        await message.channel.send(response_message.format(command, channel))
        return

