from enum import Enum
from com import MessageHandler
from com.services import FileService as file
from com.SafeStr import SafeStr as s
import re as regex


COMMAND_LENGTH_2 = 2


class AdminCommands(Enum):
    ADD = '!add'
    MODIFY = '!modify'
    DELETE = '!delete'
    HELP = '!help'


COMMAND_TO_IGNORE = [AdminCommands.DELETE.value, AdminCommands.HELP.value]

help_message = ":green_circle: Available commands in chat **#" + s.safe_string('a') + "** is:\n"\
               "1) **" + s.safe_string(AdminCommands.HELP.value) + "**\n" \
               "2) **" + s.safe_string(AdminCommands.ADD.value) + "** [username] -[description]\n" \
               "3) **" + s.safe_string(AdminCommands.MODIFY.value) + "** [username] -[description]\n" \
               "4) **" + s.safe_string(AdminCommands.DELETE.value) + "** [username]"


async def process_command(message):
    handler = MessageHandler.Handler
    command_to_process = s.safe_string(message.content)

    split_message = regex.split("(\\s+-|-)", command_to_process)

    command_part = split_message[0].split(' ')
    command = command_part[0]

    if command not in COMMAND_TO_IGNORE and not s.contains(command_to_process, '-'):
        await message.channel.send(":x: Did you forget about mark:'-'? :thinking:")
        return

    if command == AdminCommands.HELP.value:
        await message.channel.send(help_message)
        return

    if not await handler.is_message_length_valid(message, command_part, COMMAND_LENGTH_2):
        return

    username = str.lower(command_part[1])
    author = s.safe_string(message.author.name)

    if command == AdminCommands.ADD.value:
        if file.get_user_data(username) != "":
            response = ":warning: Player " + username + " already exist in black list. Instead of adding new " \
                       "one maybe consider to use command **" + AdminCommands.MODIFY.value + "**? :woozy_face:"
            await message.channel.send(response)
            return
        description_reason = split_message[2]
        if file.add_user_to_bl(author, username, description_reason):
            response = ":green_circle: Player **" + s.safe_string(username) + \
                      "** has been added to black list! :heart:"
            await message.channel.send(response)
        else:
            response = ":x: Unable to add **" + s.safe_string(username) + "** to black list! :broken_heart:"
            await message.channel.send(response)
        return

    elif command == AdminCommands.MODIFY.value:
        if file.get_user_data(username) == "":
            response = ":x: Player " + username + " to modify **not found** :cry:"
            await message.channel.send(response)
            return
        description_reason = split_message[2]
        if file.update_user_data(author, username, description_reason):
            response = ":green_circle: Player **" + username + "** has beem updated! :heart:"
            await message.channel.send(response)
        else:
            response = ":x: Unable to update **" + username + "**! :broken_heart:"
            await message.channel.send(response)
        return

    elif command == AdminCommands.DELETE.value:
        if file.remove_user_from_bl(username):
            response = ":green_circle: Player **" + username + "** has been removed from black list! :heart:"
            await message.channel.send(response)
        else:
            response = ":x: Unable to remove **" + username + "** from black list! :broken_heart:"
            await message.channel.send(response)
        return

    else:
        response_message = ":x: Unable to resolve command **'" + command + "'**. \n\n" + help_message
        await message.channel.send(response_message)
        return
