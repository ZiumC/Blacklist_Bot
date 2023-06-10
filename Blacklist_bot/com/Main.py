from MessageHandler import Handler
from services import PublicService
from services import AdminService
import discord
import os

DISCORD_TOKEN = os.getenv('DiscordToken')
PRIVATE_CHANNEL = 'private'
ADMINISTRATIVE_ROLE = 'nowa rola'
BL_PUBLIC_CHANNEL = 'ogólny'
BL_MODERATE_CHANNEL = 'moderacja'

intent = discord.Intents.default()
intent.message_content = True

client = discord.Client(intents=intent)


@client.event
async def on_ready():
    print('Discord bot runs as {}'.format(client.user))


@client.event
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
        response_message = "Sorry but command: '{}' doesn't start with '!'".format(message.content)
        await message.channel.send(response_message)
        return

    # handling public channel
    if message.channel.name == BL_PUBLIC_CHANNEL:

        await PublicCommands.process_command(message, BL_PUBLIC_CHANNEL)
        return

    # handling moderation channel
    elif message.channel.name == BL_MODERATE_CHANNEL:
        if Handler.is_authorized(message, ADMINISTRATIVE_ROLE):

            await AdministrativeCommands.process_command(message, BL_MODERATE_CHANNEL)
            return

        else:
            response_message = ":no_entry: Sorry {} but you are unauthorized to do that."
            await message.channel.send(response_message.format(message.author.name))
            return
    else:
        response_message = ":octagonal_sign: Sorry, I can only answer on channels {} or {}."
        await message.channel.send(response_message.format(BL_PUBLIC_CHANNEL, BL_MODERATE_CHANNEL))
        return

client.run(DISCORD_TOKEN)
