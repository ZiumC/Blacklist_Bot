from src.safe_str import SafeStr as s


class Handler:

    @staticmethod
    def validate_message():
        return True

    @staticmethod
    async def is_message_length_valid(message, split_message, message_length):
        if len(split_message) != message_length:
            response_message = ":x: Command **" + s.safe_string(split_message[0]) \
                               + "** accepts only " + s.safe_string(message_length) + " parameters but got " \
                               + s.safe_string(len(split_message)) + "."

            await message.channel.send(response_message)
            return False
        return True

    @staticmethod
    def is_private_channel(message, channel_type):
        for channel in message.channel.type:
            if channel == channel_type:
                return True
        return False

    @staticmethod
    def is_authorized(message, role):
        for user_role in message.author.roles:
            if user_role.name == role:
                return True
        return False

    @staticmethod
    def divide_message(message_to_divide, max_message_length=1000):
        message_chunks = []
        message_chunk = ""
        position = 0
        for i in range(0, len(message_to_divide)):
            message_chunk += message_to_divide[i]
            position += 1
            if position > max_message_length:
                message_chunks.append(message_chunk)
                message_chunk = ""
                position = 0
        message_chunks.append(message_chunk)
        return message_chunks
