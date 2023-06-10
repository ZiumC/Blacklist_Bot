class Handler:

    @staticmethod
    def validate_message():
        return True

    @staticmethod
    async def is_message_length_valid(message, split_message, message_length):
        if len(split_message) != message_length:
            response_message = ":x: Command **{}** accepts only {} parameters but got {}."
            await message.channel.send(response_message.format(split_message[0],
                                                               message_length,
                                                               len(split_message)))
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
