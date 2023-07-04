import os
import discord
from discord.ext import commands
import src.config as conf
import src.services.admin_service as adm
import src.services.public_command_service as pub
from src.message_handler import Handler as messHandler
from src.safe_str import SafeStr as sStr
import logging

intent = discord.Intents.default()
intent.message_content = True

client = discord.Client(intents=intent)


exception_response = "Something has been fucked so hard that exception has occurred :angry: Ask Toxic Rafal to see bot log."


@client.event
async def on_ready():
    print('Discord bot runs as {}'.format(client.user))


@client.event
@commands.cooldown(1, conf.MAX_REQUEST_PROCESS_TIME, commands.BucketType.user)
@commands.guild_only()
async def on_message(message):
    if message.author == client.user:
        return

    author = message.author.name

    # checking if sent message comes from private channel
    if messHandler.is_private_channel(message, conf.PRIVATE_CHANNEL):
        logging.warning("Message comes from private channel: user=" + author)
        response_message = ":x: Sorry but I can't handle private messages."
        await message.channel.send(response_message)
        return

    # checking if command starts with special character
    if not message.content.startswith('!'):
        logging.warning(
            "Message doesn't start with '!': user=" + author
            + ",message=" + sStr.safe_string(message.content, author)
        )
        response_message = ":x: Sorry but command doesn't start with '!'"
        await message.channel.send(response_message)
        return

    # handling public channel
    if message.channel.name == conf.PUBLIC_CHANNEL_BL:
        try:
            logging.info("Public command has been used: user=" + author + ",message=" + message.content)
            await pub.process_command(message, conf.PUBLIC_CHANNEL_BL)
            return
        except Exception as e:
            logging.error(
                "Public command error: user=" + author
                + ",message=" + sStr.safe_string(message.content, author)
            )
            logging.exception(e)
            await message.channel.send(exception_response)

    # handling moderation channel
    elif message.channel.name == conf.MODERATION_CHANNEL_BL:
        try:
            if messHandler.is_authorized(message, conf.ADMINISTRATIVE_ROLE):
                logging.info(
                    "Moderation command: user=" + author + ",authorization=SUCCESS, message=" + message.content
                )
                await adm.process_command(message)
                return
            else:
                logging.warning(
                    "Moderation command: user=" + author + ",authorization=FAILED, message=" + message.content
                )
                response_message = ":no_entry: Sorry but you are unauthorized to do that."
                await message.channel.send(response_message)
                return
        except Exception as e:
            logging.error(
                "Private command error: user=" + author
                + ",message=" + sStr.safe_string(message.content, author)
            )
            logging.exception(e)
            await message.channel.send(exception_response)
    else:
        logging.error("Channel miss match: channel=" + message.channel.name)
        response_message = ":octagonal_sign: Sorry, I can only answer on channels " \
                           + conf.PUBLIC_CHANNEL_BL + " or " + conf.MODERATION_CHANNEL_BL + "."
        await message.channel.send(response_message)
        return

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    filename=conf.PATH_TO_LOG_FILE
)

logging.info("---- new run ----")
client.run(os.getenv('DiscordToken'))
