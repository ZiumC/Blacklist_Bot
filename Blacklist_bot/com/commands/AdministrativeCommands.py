from enum import Enum


class AdministrativeCommands(Enum):
    ADD = '!add'
    MODIFY = '!modify'
    DELETE = '!delete'


async def process_command(message, channel_name):
    split_message = message.content.split(' ')

    if len(split_message) != 3:
        response_message = ":x: Sorry I accept only 3 parameters but passed {}. \n\n" \
                           ":arrow_forward: Input i have received: {}."
        await message.channel.send(response_message.format(len(split_message), message.content))
        return

    command = split_message[0]
    username = split_message[1]
    description = split_message[2]

    if command == AdministrativeCommands.ADD.value:
        await message.channel.send('Add new person')
        return
    elif command == AdministrativeCommands.MODIFY.value:
        await message.channel.send('Modify person')
        return
    elif command == AdministrativeCommands.DELETE.value:
        await message.channel.send('Delete person')
        return
    else:
        response_message = ":x: Unable to resolve command **'{}'**. \n\n" \
                           ":green_circle: Available commands in chat **#{}** is:\n" \
                           "1) **{}** [username] [description]\n" \
                           "2) **{}** [username] [description]\n" \
                           "3) **{}** [username]"
        await message.channel.send(response_message.format(command, channel_name,
                                                           AdministrativeCommands.ADD.value,
                                                           AdministrativeCommands.MODIFY.value,
                                                           AdministrativeCommands.DELETE.value))
        return
