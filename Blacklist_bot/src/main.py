from discord.ext import commands
from src.safe_str import SafeStr as safe_string
from src.message_handler import Handler
from typing import Final
import src.services.public_command_service as public_command
from src.services import admin_service as admin_command
import discord
import os

DISCORD_TOKEN: Final[str] = os.getenv('DiscordToken')
PRIVATE_CHANNEL: Final[str] = 'private'
ADMINISTRATIVE_ROLE: Final[str] = 'nowa rola'
BL_PUBLIC_CHANNEL: Final[str] = 'ogólny'
BL_MODERATE_CHANNEL: Final[str] = 'moderacja'
PATH_TO_BLOCKED_USERS_FILE: Final[str] = os.getenv('PATH_TO_BLOCKED_USERS_FILE')
PATH_TO_LOG_FILE: Final[str] = os.getenv('PATH_TO_LOG_FILE')
MAX_MESSAGE_LENGTH = 1999

intent = discord.Intents.default()
intent.message_content = True

client = discord.Client(intents=intent)


@client.event
async def on_ready():
    print('Discord bot runs as {}'.format(client.user))


@client.event
@commands.cooldown(1, 30, commands.BucketType.user)
@commands.guild_only()
async def on_message(message):
    if message.author == client.user:
        return

    # checking if sent message comes from private channel
    if Handler.is_private_channel(message, PRIVATE_CHANNEL):
        response_message = ":x: Sorry but I can't handle private messages."
        await message.channel.send(response_message)
        return

    # checking if command starts with special character
    if not message.content.startswith('!'):
        response_message = ":x: Sorry but command doesn't start with '!'"
        await message.channel.send(response_message)
        return

    # handling public channel
    if message.channel.name == BL_PUBLIC_CHANNEL:
        # try:
            await public_command.process_command(message, BL_PUBLIC_CHANNEL)
            return
        # except Exception as e:
        #     await message.channel.send("What the fuck are you doing you little piece of shit? :angry:")

    # handling moderation channel
    elif message.channel.name == BL_MODERATE_CHANNEL:
        # try:
            if Handler.is_authorized(message, ADMINISTRATIVE_ROLE):

                await admin_command.process_command(message)
                return

            else:
                response_message = ":no_entry: Sorry but you are unauthorized to do that."
                await message.channel.send(response_message)
                return
        # except Exception as e:
        #     await message.channel.send("What the fuck are you doing you little piece of shit? :angry:")
    else:
        response_message = ":octagonal_sign: Sorry, I can only answer on channels " \
                           + safe_string.safe_string(BL_PUBLIC_CHANNEL) + " or " + safe_string.safe_string(BL_MODERATE_CHANNEL) + "."
        await message.channel.send(response_message)
        return


client.run(DISCORD_TOKEN)
