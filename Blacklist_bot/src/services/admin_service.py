import re as regex
from enum import Enum
import src.config as conf
from src.services import file_service
from src.safe_str import SafeStr as sStr
from src.message_handler import Handler as messHandler


class AdminCommands(Enum):
    ADD = '!add'
    MODIFY = '!modify'
    DELETE = '!delete'
    HELP = '!help'


COMMANDS_TO_IGNORE = [AdminCommands.DELETE.value, AdminCommands.HELP.value]

help_message = ":green_circle: Available commands in chat **#" + conf.MODERATION_CHANNEL_BL + "** is:\n"\
               "1) **" + AdminCommands.HELP.value + "**\n" \
               "2) **" + AdminCommands.ADD.value + "** [username] -[description]\n" \
               "3) **" + AdminCommands.MODIFY.value + "** [username] -[description]\n" \
               "4) **" + AdminCommands.DELETE.value + "** [username]"


async def process_command(message):
    command_to_process = sStr.safe_string(message.content)

    split_message = regex.split("(\\s+-|-)", command_to_process)

    command_part = split_message[0].split(' ')
    command = command_part[0]

    if command not in COMMANDS_TO_IGNORE and not messHandler.contains(command_to_process, '-'):
        await message.channel.send(":x: Did you forget about mark:'-'? :thinking:")
        return

    if command == AdminCommands.HELP.value:
        await message.channel.send(help_message)
        return

    if not await messHandler.is_message_length_valid(message, command_part, conf.MAX_COMMAND_LENGTH):
        return

    author = sStr.safe_string(message.author.name)
    username = str.lower(command_part[1])

    if command == AdminCommands.ADD.value:
        if file_service.get_user_data(username) != "":
            response = ":warning: Player **" + username + "** already exist in black list. Instead of adding new " \
                       "one maybe consider to use command **" + AdminCommands.MODIFY.value + "**? :woozy_face:"
            await message.channel.send(response)
            return
        description_reason = split_message[2]
        if file_service.add_user_to_bl(author, username, description_reason):
            response = ":green_circle: Player **" + username + \
                      "** has been added to black list! :heart:"
            await message.channel.send(response)
        else:
            response = ":x: Unable to add **" + username + "** to black list! :broken_heart:"
            await message.channel.send(response)
        return

    elif command == AdminCommands.MODIFY.value:
        if file_service.get_user_data(username) == "":
            response = ":x: Player **" + username + "** to modify **not found** :cry:"
            await message.channel.send(response)
            return
        description_reason = split_message[2]
        if file_service.update_user_data(author, username, description_reason):
            response = ":green_circle: Player **" + username + "** has beem updated! :heart:"
            await message.channel.send(response)
        else:
            response = ":x: Unable to update **" + username + "**! :broken_heart:"
            await message.channel.send(response)
        return

    elif command == AdminCommands.DELETE.value:
        if file_service.get_user_data(username) == "":
            response = ":x: Player **" + username + "** to delete **not found** :cry:"
            await message.channel.send(response)
            return
        if file_service.remove_user_from_bl(username):
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
