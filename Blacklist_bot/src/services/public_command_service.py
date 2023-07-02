from enum import Enum
from src.services import file_service as file
from src.safe_str import SafeStr as s
from src.message_handler import Handler
from src import main as m


class PublicCommands(Enum):
    CHECK = "!check"


async def process_command(message, channel_name):
    safe_string = s.safe_string(message.content)
    split_message = safe_string.split(' ')

    if len(split_message) != 2:
        response_message = ":x: Sorry I accept only 2 parameters but passed " + s.safe_string(len(split_message)) + "."
        await message.channel.send(response_message)
        return

    command = split_message[0]
    username = str.lower(split_message[1])

    if command == PublicCommands.CHECK.value:
        user_data = file.get_user_data(username)
        if user_data != "":
            sections_data = user_data.split(",")
            response = ":octagonal_sign: Player **" + username + \
                       "** exist on black list! :face_with_symbols_over_mouth:\n\n " \
                       ":information_source: Player **" + username + "** has been added to black list by **" \
                       + sections_data[3] + "** at **" + sections_data[2] + "**.\n"
            await message.channel.send(response)
            reason = ":arrow_right: Reason: " + sections_data[1]
            if len(reason) > m.MAX_MESSAGE_LENGTH:
                reason_chunks = Handler.divide_message(reason, m.MAX_MESSAGE_LENGTH)
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
        response_message = ":x: Unable to resolve command **'" \
                           + s.safe_string(command) + "'**. \n\n" \
                            ":green_circle: Available commands in chat **#" + s.safe_string(channel_name) + "** is:\n" \
                            "1) **" + PublicCommands.CHECK.value + "** [username]"
        await message.channel.send(response_message)
        return
