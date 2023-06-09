import discord
import os
from MessageHandler import Handler

DISCORD_TOKEN = os.getenv('DiscordToken')
SERVER_CHANNEL_NAME = 'ogólny'

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

    if not message.content.startswith('/'):
        response = "Sorry but command: '{}' doesn't start at '/'".format(message.content)
        await message.channel.send(response)
        return

    if Handler.is_private_channel(message):
        await message.channel.send("Private channel!")
        return
    else:
        if message.channel.name == SERVER_CHANNEL_NAME:
            if message.content == '$hello':
                await message.channel.send('Hello!')
                return
            else:
                response = "Sorry, I dont know what is '{}'."
                await message.channel.send(response.format(message.content))
                return
        else:
            response = "Sorry, I can only answer on channel {} or private messages."
            await message.channel.send(response.format(SERVER_CHANNEL_NAME))
            return 


client.run(DISCORD_TOKEN)
