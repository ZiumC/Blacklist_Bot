import logging
from enum import Enum
import config as conf
from parsers import armory_character_parser as armory_parser
from services import file_service
from safe_str import SafeStr as sStr
from message_handler import Handler as messHandler


class PublicCommands(Enum):
    CHECK = "!check"
    HELP = "!help"


COMMANDS_TO_IGNORE = [PublicCommands.HELP.value]

help_message = ":green_circle: Available commands in chat **#" + conf.PUBLIC_CHANNEL_BL + "** is:\n" \
                "1) **" + PublicCommands.HELP.value + "**\n" \
                "2) **" + PublicCommands.CHECK.value + "** [username]"


async def process_command(message, channel_name):
    author = message.author.name
    safe_string = sStr.safe_string(message.content, author)
    split_message = safe_string.split(' ')

    command = split_message[0]
    # this is unsafe string!
    # it is needed due to get original player name
    original_username = message.content.split(' ')[1]

    if command == PublicCommands.HELP.value:
        await message.channel.send(help_message)
        return

    if not await messHandler.is_message_length_valid(message, split_message, conf.MAX_PUBLIC_COMMAND_LENGTH):
        logging.warning(
            "Command length missmatch: user=" + author + ",current_length=" + str(len(split_message))
            + ",accepted_length=" + str(conf.MAX_PUBLIC_COMMAND_LENGTH)
        )
        return

    username = str.lower(split_message[1])

    if command == PublicCommands.CHECK.value:
        user_data = file_service.get_user_data(username)
        if user_data != "":
            sections_data = user_data.split(conf.SEPARATOR)
            response = ":octagonal_sign: Player **" + username + \
                       "** exist on black list! :face_with_symbols_over_mouth:\n\n " \
                       ":information_source: Player **" + username + "** has been added to black list by **" \
                       + sections_data[3] + "** at **" + sections_data[2] + "**.\n"
            await message.channel.send(response)
            reason = ":arrow_right: Reason: " + sections_data[1]
            if len(reason) > conf.MAX_DISCORD_MESSAGE_LENGTH:
                logging.info("Response reason was split")
                reason_chunks = messHandler.divide_message(reason, conf.MAX_DISCORD_MESSAGE_LENGTH)
                for reason_line in reason_chunks:
                    await message.channel.send(reason_line)
            else:
                await message.channel.send(reason)
                armory_parser.get_player_items(original_username)
            return
        else:
            logging.info("Searched player not found (this is good)")
            response = ":white_check_mark: Player **not found!**"
            await message.channel.send(response)
            return
    else:
        logging.error("Command missmatch: user=" + author + ",full_command=" + safe_string)
        response_message = ":x: Unable to resolve command **'" + command + "'**.\n\n" + help_message
        await message.channel.send(response_message)
        return
