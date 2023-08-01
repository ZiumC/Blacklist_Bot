import logging
import re as regex
from enum import Enum
import config as conf
from services import file_service
from safe_str import SafeStr as sStr
from message_handler import Handler as messHandler


class AdminCommands(Enum):
    ADD = '!add'
    MODIFY = '!modify'
    DELETE = '!delete'
    LAST = '!last'
    HELP = '!help'



COMMANDS_TO_IGNORE = [AdminCommands.DELETE.value, AdminCommands.HELP.value, AdminCommands.LAST.value]

help_message = ":green_circle: Available commands in chat **#" + conf.MODERATION_CHANNEL_BL + "** is:\n"\
               "1) **" + AdminCommands.HELP.value + "**\n" \
               "2) **" + AdminCommands.ADD.value + "** [username] -[description]\n" \
               "3) **" + AdminCommands.MODIFY.value + "** [username] -[description]\n" \
               "4) **" + AdminCommands.DELETE.value + "** [username]\n" \
               "5) **" + AdminCommands.LAST.value + "**\n" \
               ":large_blue_diamond: If you want write only announce message, just type character **$** before your message and bot will ignore it."


async def process_command(message):
    author_unsafe = message.author.name
    command_to_process = sStr.safe_string(message.content, author_unsafe)

    split_message = regex.split("(\\s+-|-)", command_to_process)

    command_part = split_message[0].split(' ')
    command = command_part[0]

    if command not in COMMANDS_TO_IGNORE and not messHandler.contains(command_to_process, '-'):
        logging.warning("Incorrect command format: user=" + author_unsafe + ",full_command=" + command_to_process)
        await message.channel.send(":x: Did you forget about mark:'-'? :thinking:")
        return

    if command == AdminCommands.HELP.value:
        await message.channel.send(help_message)
        return
    if command == AdminCommands.LAST.value:
        last_user_data = file_service.get_last_user_data()
        sections_data = last_user_data  .split(",")
        last_user_name = sections_data[0]
        response = ":orange_circle: Last added player to blacklist is **" + last_user_name + "**.\n\n" \
                   ":information_source: Player has been added by **" + sections_data[3] + "** at **" + sections_data[2] + "**.\n" \
                   ":arrow_right: Reason: " + sections_data[1]
        logging.info("Checking last player: user=" + author_unsafe + ",last player=" + last_user_name)
        await message.channel.send(response)
        return

    if not await messHandler.is_message_length_valid(message, command_part, conf.MAX_MODERATION_COMMAND_LENGTH):
        logging.warning(
            "Command length missmatch: user=" + author_unsafe + ",current_length=" + str(len(command_part))
            + ",accepted_length=" + str(conf.MAX_MODERATION_COMMAND_LENGTH) + ",full_command=" + command_to_process
        )
        return

    author_safe = sStr.safe_string(author_unsafe, author_unsafe)
    username = str.lower(command_part[1])

    if command == AdminCommands.ADD.value:
        if file_service.get_user_data(username) != "":
            response = ":warning: Player **" + username + "** already exist in blacklist. Instead of adding new " \
                       "one maybe consider to use command **" + AdminCommands.MODIFY.value + "**? :woozy_face:"
            await message.channel.send(response)
            return
        description_reason = split_message[2]
        if file_service.add_user_to_bl(author_safe, username, description_reason):
            response = ":green_circle: Player **" + username + \
                      "** has been added to blacklist! :heart:"
            logging.info("Added to BL: user=" + author_unsafe + ",player=" + username)
            await message.channel.send(response)
        else:
            response = ":x: Unable to add **" + username + "** to blacklist! :broken_heart:"
            logging.warning(
                "Unable to add to BL: user=" + author_unsafe + ",player="
                + username + ",full_command=" + command_to_process
            )
            await message.channel.send(response)
        return

    elif command == AdminCommands.MODIFY.value:
        if file_service.get_user_data(username) == "":
            response = ":x: Player **" + username + "** to modify **not found** :cry:"
            logging.warning(
                "Player to update not found: user=" + author_unsafe + ",player="
                + username + ",full_command=" + command_to_process
            )
            await message.channel.send(response)
            return
        description_reason = split_message[2]
        if file_service.update_user_data(author_safe, username, description_reason):
            response = ":green_circle: Player **" + username + "** has beem updated! :heart:"
            logging.info("Updated player in BL: user=" + author_unsafe + ",player=" + username)
            await message.channel.send(response)
        else:
            response = ":x: Unable to update **" + username + "**! :broken_heart:"
            logging.warning(
                "Unable to update player in BL: user=" + author_unsafe + ",player="
                + username + ",full_command=" + command_to_process
            )
            await message.channel.send(response)
        return

    elif command == AdminCommands.DELETE.value:
        if file_service.get_user_data(username) == "":
            response = ":x: Player **" + username + "** to delete **not found** :cry:"
            logging.warning(
                "Player to delete not found: user=" + author_unsafe + ",player="
                + username + ",full_command=" + command_to_process
            )
            await message.channel.send(response)
            return
        if file_service.remove_user_from_bl(username):
            response = ":green_circle: Player **" + username + "** has been removed from blacklist! :heart:"
            logging.info("Deleted player from BL: user=" + author_unsafe + ",player=" + username)
            await message.channel.send(response)
        else:
            response = ":x: Unable to remove **" + username + "** from blacklist! :broken_heart:"
            logging.warning(
                "Unable do delete player from BL: user=" + author_unsafe + ",player="
                + username + ",full_command=" + command_to_process
            )
            await message.channel.send(response)
        return

    else:
        logging.error("Command missmatch: user=" + author_unsafe + ",full_command=" + command_to_process)
        response_message = ":x: Unable to resolve command **'" + command + "'**. \n\n" + help_message
        await message.channel.send(response_message)
        return
