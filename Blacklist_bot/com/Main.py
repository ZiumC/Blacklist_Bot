import discord
import os

DISCORD_TOKEN = os.getenv('DiscordToken')
SERVER_CHANNEL_NAME = 'ogólny'

intent = discord.Intents.default()
intent.message_content = True

client = discord.Client(intents=intent)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.name == "ogólny":
        if message.content == '$hello':
            await message.channel.send('Hello!')
        else:
            await message.channel.send('Sorry, I dont know what is it')


client.run(DISCORD_TOKEN)
