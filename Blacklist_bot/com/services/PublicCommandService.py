from enum import Enum
from com.services import FileService as file
from com.SafeStr import SafeStr as s


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
            response = ":octagonal_sign: Player **" + username + \
                       "** exist on black list! :face_with_symbols_over_mouth:\n\n"
            await message.channel.send(response)
            sections_data = user_data.split(",")
            header_reason = ":information_source: Player **" + username + "** has been added to black list by **" \
                            + sections_data[3] + "** at **" + sections_data[2] + "**.\n"
            await message.channel.send(header_reason)
            reason = ":arrow_right: Reason: " + sections_data[1]
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
                            "1) **" + s.safe_string(PublicCommands.CHECK.value) + "** [username]"
        await message.channel.send(response_message)
        return
