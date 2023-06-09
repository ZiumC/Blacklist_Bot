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

    if Handler.is_private_channel(message):
        await message.channel.send('Private channel!')
    else:
        if message.channel.name == SERVER_CHANNEL_NAME:
            if message.content == '$hello':
                await message.channel.send('Hello!')
            else:
                response = "Sorry, I dont know what is '{}'."
                await message.channel.send(response.format(message.content))
        else:
            response = "Sorry, I can only answer on channel {} or private messages."
            await message.channel.send(response.format(SERVER_CHANNEL_NAME))


client.run(DISCORD_TOKEN)
