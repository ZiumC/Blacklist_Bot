import os
import discord
from discord.ext import commands
import src.config as conf
import src.services.admin_service as adm
import src.services.public_command_service as pub
from src.message_handler import Handler as messHandler

intent = discord.Intents.default()
intent.message_content = True

client = discord.Client(intents=intent)


exception_response = "Your action that you are trying to perform is too shitty :angry: Ask Toxic Rafal to see bot log."


@client.event
async def on_ready():
    print('Discord bot runs as {}'.format(client.user))


@client.event
@commands.cooldown(1, conf.MAX_REQUEST_PROCESS_TIME, commands.BucketType.user)
@commands.guild_only()
async def on_message(message):
    if message.author == client.user:
        return

    # checking if sent message comes from private channel
    if messHandler.is_private_channel(message, conf.MODERATION_CHANNEL_BL):
        response_message = ":x: Sorry but I can't handle private messages."
        await message.channel.send(response_message)
        return

    # checking if command starts with special character
    if not message.content.startswith('!'):
        response_message = ":x: Sorry but command doesn't start with '!'"
        await message.channel.send(response_message)
        return

    # handling public channel
    if message.channel.name == conf.PUBLIC_CHANNEL_BL:
        try:
            await pub.process_command(message, conf.PUBLIC_CHANNEL_BL)
            return
        except Exception as e:
            await message.channel.send(exception_response)

    # handling moderation channel
    elif message.channel.name == conf.MODERATION_CHANNEL_BL:
        try:
            if messHandler.is_authorized(message, conf.ADMINISTRATIVE_ROLE):
                await adm.process_command(message)
                return
            else:
                response_message = ":no_entry: Sorry but you are unauthorized to do that."
                await message.channel.send(response_message)
                return
        except Exception as e:
            await message.channel.send(exception_response)
    else:
        response_message = ":octagonal_sign: Sorry, I can only answer on channels " \
                           + conf.PUBLIC_CHANNEL_BL + " or " + conf.MODERATION_CHANNEL_BL + "."
        await message.channel.send(response_message)
        return


client.run(os.getenv('DiscordToken'))
