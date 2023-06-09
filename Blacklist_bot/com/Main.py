from MessageHandler import Handler
from commands import PublicCommands
import discord
import os

DISCORD_TOKEN = os.getenv('DiscordToken')
ADMINISTRATIVE_ROLE = 'nowa rola'
SERVER_PUBLIC_CHANNEL_BL = 'ogólny'
SERVER_MODERATE_CHANNEL_BL = 'moderacja'

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

    # checking if command starts with special character
    if not message.content.startswith('!'):
        response_message = "Sorry but command: '{}' doesn't start with '!'".format(message.content)
        await message.channel.send(response_message)
        return

    # checking if sent message comes from private channel
    if Handler.is_private_channel(message):
        response_message = "Sorry but I can't handle private messages."
        await message.channel.send(response_message)
        return

    # handling public channel
    if message.channel.name == SERVER_PUBLIC_CHANNEL_BL:

        await PublicCommands.process_command(message, SERVER_PUBLIC_CHANNEL_BL)

    # handling moderation channel
    elif message.channel.name == SERVER_MODERATE_CHANNEL_BL:
        if Handler.is_authorized(message, ADMINISTRATIVE_ROLE):

            return
        else:
            response_message = "Sorry but you are unauthorized to do that."
            message.channel.send(response_message)
            return
    else:
        response_message = "Sorry, I can only answer on channels {} or {}."
        await message.channel.send(response_message.format(SERVER_PUBLIC_CHANNEL_BL, SERVER_MODERATE_CHANNEL_BL))
        return

client.run(DISCORD_TOKEN)
