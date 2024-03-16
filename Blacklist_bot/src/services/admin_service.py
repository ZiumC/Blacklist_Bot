import logging
import re as regex
from enum import Enum
import config as conf
from services import file_service
from services import log_service
from utils.safe_str_util import SafeStr as sStr
from message_handler import Handler as messHandler
from services.message_formatter_service import AdminCommandFormatter as admF


class AdminCommands(Enum):
    ADD = '!add'
    MODIFY = '!modify'
    DELETE = '!delete'
    LAST = '!last'
    HELP = '!help'
    LOG_ERR = '!log_err'
    CLEAR_LOG = '!clear_log'


class LogErrType(Enum):
    CRITICAL = 'CRITICAL'
    ERROR = 'ERROR'
    WARNING = 'WARNING'


LOG_ERROR_TYPES = [LogErrType.CRITICAL.value, LogErrType.ERROR.value,
                   LogErrType.WARNING.value]
COMMANDS_LIST = [AdminCommands.HELP.value, AdminCommands.ADD.value,
                 AdminCommands.MODIFY.value, AdminCommands.DELETE.value,
                 AdminCommands.LAST.value, AdminCommands.LOG_ERR.value,
                 AdminCommands.CLEAR_LOG.value]
COMMANDS_TO_IGNORE = [AdminCommands.DELETE.value, AdminCommands.HELP.value,
                      AdminCommands.LAST.value, AdminCommands.LOG_ERR.value,
                      AdminCommands.CLEAR_LOG.value]


async def process_command(message):
    author_unsafe = message.author.name
    command_to_process = sStr.safe_string(message.content, author_unsafe)

    split_message = regex.split("(\\s+-|-)", command_to_process)

    command_part = split_message[0].split(' ')
    command = command_part[0]

    if command not in COMMANDS_TO_IGNORE and not messHandler.contains(command_to_process, '-'):
        logging.warning("Incorrect command format: user=" + author_unsafe + ",full_command=" + command_to_process)
        await message.channel.send(admF.format_forgotten_sign_error())
        return

    if command == AdminCommands.HELP.value:
        await message.channel.send(admF.format_help(COMMANDS_LIST))
        return

    if command == AdminCommands.LAST.value:
        last_user_data = file_service.get_last_user_data()
        sections_data = last_user_data.split(conf.SEPARATOR)

        if len(sections_data) <= 1:
            logging.warning('Black list is empty!')
            await message.channel.send(admF.format_players_notfound_error())
            return

        last_user_name = sections_data[0]
        response_messages = admF.format_last_added(last_user_name, sections_data[3], sections_data[2], sections_data[1])

        for response_message in response_messages:
            await message.channel.send(response_message)
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
            await message.channel.send(admF.format_player_exist_error(username, AdminCommands.MODIFY.value))
            return
        description_reason = split_message[2]
        if file_service.add_user_to_bl(author_safe, username, description_reason):
            await message.channel.send(admF.format_add_success(username))
        else:
            await message.channel.send(admF.format_command_error(username, command))
        return

    elif command == AdminCommands.MODIFY.value:
        if file_service.get_user_data(username) == "":
            await message.channel.send(admF.format_notfound_error(username))
            return
        description_reason = split_message[2]
        if file_service.update_user_data(author_safe, username, description_reason):
            await message.channel.send(admF.format_update_success(username))
        else:
            await message.channel.send(admF.format_command_error(username, command))
        return

    elif command == AdminCommands.DELETE.value:
        if file_service.get_user_data(username) == "":
            await message.channel.send(admF.format_notfound_error(username))
            return
        if file_service.remove_user_from_bl(username):
            await message.channel.send(admF.format_delete_success(username))
        else:
            await message.channel.send(admF.format_command_error(username, command))
        return

    elif command == AdminCommands.LOG_ERR.value:
        given_log_type = command_part[1].upper()
        if given_log_type in LOG_ERROR_TYPES:
            warning_log_lines = log_service.get_log_lines_by(given_log_type)
            response_messages = admF.format_log_output(given_log_type.upper(), warning_log_lines)
            for response_line in response_messages:
                await message.channel.send(response_line)
            return
        else:
            logging.error("Log type missmatch: user=" + author_safe + ",full_command=" + command_to_process)
            await message.channel.send(admF.format_unknown_command_error(command_to_process, COMMANDS_LIST))
            return

    else:
        logging.error("Command missmatch: user=" + author_safe + ",full_command=" + command_to_process)
        await message.channel.send(admF.format_unknown_command_error(command, COMMANDS_LIST))
        return
