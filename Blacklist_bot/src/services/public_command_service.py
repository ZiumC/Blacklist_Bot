from enum import Enum
import src.config as conf
from src.services import file_service
from src.safe_str import SafeStr as sStr
from src.message_handler import Handler as messHandler
import logging


class PublicCommands(Enum):
    CHECK = "!check"


async def process_command(message, channel_name):
    safe_string = sStr.safe_string(message.content)
    split_message = safe_string.split(' ')

    mess_length = len(split_message)
    if mess_length != conf.MAX_PUBLIC_COMMAND_LENGTH:
        logging.warning(
            "Command length missmatch: user=" + message.author.name + ",current_length=" + str(mess_length)
            + ",accepted_length=" + str(conf.MAX_PUBLIC_COMMAND_LENGTH)
        )
        response_message = ":x: Sorry I accept only 2 parameters but passed " \
                           + str(len(split_message)) + "."
        await message.channel.send(response_message)
        return

    command = split_message[0]
    username = str.lower(split_message[1])

    if command == PublicCommands.CHECK.value:
        user_data = file_service.get_user_data(username)
        if user_data != "":
            sections_data = user_data.split(",")
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
            return
        else:
            response = ":white_check_mark: Player **not found!**"
            await message.channel.send(response)
            return

    else:
        logging.error("Command missmatch: user=" + message.author.name + ",full_command=" + safe_string)
        response_message = ":x: Unable to resolve command **'" + command + \
                           "'**. \n\n :green_circle: Available commands in chat **#" + \
                           sStr.safe_string(channel_name) + "** is:\n" \
                            "1) **" + PublicCommands.CHECK.value + "** [username]"
        await message.channel.send(response_message)
        return
