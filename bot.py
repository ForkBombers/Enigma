"""
This file is the main entry point of the bot
"""

from multiprocessing.util import debug
import discord
import logging
import os
import re
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import CheckFailure
from src.utils import searchSong, has_role_dj, update_vc_status, check_vc_status
from src.songs_queue import Songs_Queue
from Cogs.songs_cog import Songs

logging.basicConfig(level=logging.INFO)
load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN')
VOICE_CHANNEL_ID = 924705413172183044  # NoName VC
# 1300855852374163497 # Group 86 VC
# 1299270426794524708 # Enigma test general
# 1300499798545141873 # Hotel Quink Server
# 1300287459451736064 - SQUAD Server
# 1017135653789646851

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
intents.guilds = True

client = commands.Bot(command_prefix=']', intents=intents)

authorized_channels = []
"""
Function that gets executed once the bot is initialized
"""


def setup_bot():
    client = commands.Bot(command_prefix=']', intents=intents)

    @client.event
    async def on_ready():
        voice_channel = client.get_channel(VOICE_CHANNEL_ID)
        if client.user not in voice_channel.members:
            await voice_channel.connect()
        extensions = client.load_extension("Cogs.songs_cog")
        await extensions
        print("Enigma is online!")

    """
    Function to reconnect bot if it disconnects
    """

    @client.event
    async def on_voice_state_update(member, before, after):
        # if member == client.user and before.channel is not None and after.channel is None:
        #     print(f"{str(member.name)} disconnected from {before.channel.name}")
        #     # voice_channel = client.get_channel(VOICE_CHANNEL_ID)
        #     voice_channel = discord.utils.get(client.voice_clients, guild=before.channel.guild)

        #     # Ensure the bot only attempts to connect if it is not already connected
        #     if voice_channel and not voice_channel.is_connected():
        #         await voice_channel.connect(reconnect=True, timeout=10.0)
        await update_vc_status(client, member, before, after)

    client.add_check(check_vc_status())
    """
    Function to authorize channels 
    """
    channels_help = """
    Add allowed channels for the bot\n
    - example : ]channels <channel1>, <channel2>, ...
    """

    @client.command(name='channels', help=channels_help)
    @has_role_dj()
    async def authorize_channel(ctx):
        global authorized_channels
        user_message = str(ctx.message.content)
        extract = re.search(r"\]channels (.+)", user_message)
        if extract:
            channels_extract = [
                channel.strip() for channel in extract.group(1).split(",")
            ]
            new_channels = []
            for tc in channels_extract:
                if tc not in authorized_channels:
                    authorized_channels.append(tc)
                    new_channels.append(tc)
            if new_channels:
                new_channels_str = ", ".join(new_channels)
                await ctx.send(f"Added authorized channels: {new_channels_str}"
                               )
            else:
                await ctx.send(
                    "No new channels added. All channels have been authorized already."
                )
        else:

            if authorized_channels:
                await ctx.send(
                    f"No new channels added. \nChannels : {', '.join(f'[{ch_name}]' for ch_name in authorized_channels)}"
                )
            else:
                await ctx.send(
                    f"No new channels added. \nUse format: `]channels <channel1>, <channel2>, ...`"
                )

# """
# Function for playing a song
# """
# @client.command(name="play", help="To play a song")
# @has_role_dj()
# async def play(ctx, *, song: str):
#     await ctx.send(f"Playing {song} requested by {ctx.author.display_name}")

    """
    Function that is executed once any message is received by the bot
    """

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.channel.name in authorized_channels or message.channel.name == 'testing-space':
            await client.process_commands(message)

    """
    Error checking function that returns any error received by the bot
    """

    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, CheckFailure):
            await ctx.send("You need the DJ role to use this command!")
        else:
            print(f"An error has occurred: {error}")

    """
    Function to reconnect the bot to the VC 
    """

    @client.command(name="reconnect",
                    help="To connect the bot to voice channel")
    @has_role_dj()
    async def reconnect(ctx):
        await ctx.send("Reconnecting enigma to VC ...")
        await on_ready()

    """
    Start the bot
    """
    return client


# Create the bot instance
client = setup_bot()

if __name__ == '__main__':
    client.run(TOKEN)

# @client.event
# async def on_ready():
#     voice_channel = client.get_channel(VOICE_CHANNEL_ID)
#     if client.user not in voice_channel.members:
#         await voice_channel.connect()
#     extensions = client.load_extension("Cogs.songs_cog")
#     await extensions
#     print("Enigma is online!")

# """
# Function to reconnect bot if it disconnects
# """

# @client.event
# async def on_voice_state_update(member, before, after):
#     # if member == client.user and before.channel is not None and after.channel is None:
#     #     print(f"{str(member.name)} disconnected from {before.channel.name}")
#     #     # voice_channel = client.get_channel(VOICE_CHANNEL_ID)
#     #     voice_channel = discord.utils.get(client.voice_clients, guild=before.channel.guild)

#     #     # Ensure the bot only attempts to connect if it is not already connected
#     #     if voice_channel and not voice_channel.is_connected():
#     #         await voice_channel.connect(reconnect=True, timeout=10.0)
#     await update_vc_status(client, member, before, after)

# client.add_check(check_vc_status())
# """
# Function to authorize channels
# """
# channels_help = """
# Add allowed channels for the bot\n
# - example : ]channels <channel1>, <channel2>, ...
# """

# @client.command(name='channels', help=channels_help)
# @has_role_dj()
# async def authorize_channel(ctx):
#     global authorized_channels
#     user_message = str(ctx.message.content)
#     extract = re.search(r"\]channels (.+)", user_message)
#     if extract:
#         channels_extract = [
#             channel.strip() for channel in extract.group(1).split(",")
#         ]
#         new_channels = []
#         for tc in channels_extract:
#             if tc not in authorized_channels:
#                 authorized_channels.append(tc)
#                 new_channels.append(tc)
#         if new_channels:
#             new_channels_str = ", ".join(new_channels)
#             await ctx.send(f"Added authorized channels: {new_channels_str}")
#         else:
#             await ctx.send(
#                 "No new channels added. All channels have been authorized already."
#             )
#     else:

#         if authorized_channels:
#             await ctx.send(
#                 f"No new channels added. \nChannels : {', '.join(f'[{ch_name}]' for ch_name in authorized_channels)}"
#             )
#         else:
#             await ctx.send(
#                 f"No new channels added. \nUse format: `]channels <channel1>, <channel2>, ...`"
#             )

# # """
# # Function for playing a song
# # """
# # @client.command(name="play", help="To play a song")
# # @has_role_dj()
# # async def play(ctx, *, song: str):
# #     await ctx.send(f"Playing {song} requested by {ctx.author.display_name}")
# """
# Function that is executed once any message is received by the bot
# """

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.channel.name in authorized_channels or message.channel.name == 'testing-space':
#         await client.process_commands(message)

# """
# Error checking function that returns any error received by the bot
# """

# @client.event
# async def on_command_error(ctx, error):
#     if isinstance(error, CheckFailure):
#         await ctx.send("You need the DJ role to use this command!")
#     else:
#         print(f"An error has occurred: {error}")

# """
# Function to reconnect the bot to the VC
# """

# @client.command(name="reconnect", help="To connect the bot to voice channel")
# @has_role_dj()
# async def reconnect(ctx):
#     await ctx.send("Reconnecting enigma to VC ...")
#     await on_ready()

# """
# Start the bot
# """
# # load_extensions()
# client.run(TOKEN)
