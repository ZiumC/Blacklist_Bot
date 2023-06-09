class Handler:

    @staticmethod
    def validate_message():
        return True

    @staticmethod
    def is_private_channel(message):
        private_channel = message.channel.type[0]
        return private_channel == 'private'

    @staticmethod
    def is_authorized(message, role):
        return message.author.top_role == role
