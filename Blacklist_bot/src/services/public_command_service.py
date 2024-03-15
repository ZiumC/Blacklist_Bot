import logging
import config as conf
from services import file_service
from services.message_formatter_service import ArmoryFormatter as armoryF
from services.message_formatter_service import PublicCommandFormatter as pubF
from services.message_formatter_service import ViablePublicCommands as PublicCommands
from utils.safe_str_util import SafeStr as sStr
from message_handler import Handler as messHandler

COMMANDS_TO_IGNORE = [PublicCommands.HELP.value]


async def process_command(message, channel_name):
    author = message.author.name
    safe_string = sStr.safe_string(message.content, author)
    split_message = safe_string.split(' ')

    command = split_message[0]

    if command == PublicCommands.HELP.value:
        await message.channel.send(pubF.format_help())
        return

    if not await messHandler.is_message_length_valid(message, split_message, conf.MAX_PUBLIC_COMMAND_LENGTH):
        logging.warning(
            "Command length missmatch: user=" + author + ",current_length=" + str(len(split_message))
            + ",accepted_length=" + str(conf.MAX_PUBLIC_COMMAND_LENGTH)
        )
        return

    username = str.lower(split_message[1])
    username_warmane_style = __get_username_warmane_style(username)

    if command == PublicCommands.CHECK.value:
        user_data = file_service.get_user_data(username)
        if user_data != "":
            sections_data = user_data.split(conf.SEPARATOR)
            response = pubF.format_bl_warning(username_warmane_style, sections_data[3], sections_data[2])
            await message.channel.send(response)

            reason_response = pubF.format_bl_reason(sections_data[1])
            for message_line in reason_response:
                await message.channel.send(message_line)
            return
        else:
            response_messages = pubF.format_bl_notfound()
            for response_message in response_messages:
                await message.channel.send(response_message)

            armory_messages = armoryF.get_messages_of(username_warmane_style)
            if len(armory_messages) > 0:
                for armory_response in armory_messages:
                    await message.channel.send(armory_response)
            return
    else:
        logging.error("Command missmatch: user=" + author + ",full_command=" + safe_string)
        await message.channel.send(pubF.format_error(command))
        return


def __get_username_warmane_style(username):
    return username.title()
