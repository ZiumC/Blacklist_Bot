class Handler:

    @staticmethod
    def validate_message():
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
