"""
This file is the main entry point of the bot
"""

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
from src.get_all import recommend  # Import recommend function to generate new song list

logging.basicConfig(level=logging.INFO)
load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN')
VOICE_CHANNEL_ID = 924705413172183044  # NoName VC

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
    # Remove the duplicate bot initialization
    bot = commands.Bot(command_prefix=']', intents=intents)

    @bot.event
    async def on_ready():
        voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
        if bot.user not in voice_channel.members:
            await voice_channel.connect()
        await bot.load_extension("Cogs.songs_cog")
        print("Enigma is online!")

    @bot.event
    async def on_voice_state_update(member, before, after):
        await update_vc_status(bot, member, before, after)

    bot.add_check(check_vc_status())

    """
    Function to authorize channels 
    """
    @bot.command(name='channels', help="Add allowed channels for the bot\n- example: ]channels <channel1>, <channel2>, ...")
    @has_role_dj()
    async def authorize_channel(ctx):
        global authorized_channels
        user_message = str(ctx.message.content)
        extract = re.search(r"\]channels (.+)", user_message)
        if extract:
            channels_extract = [channel.strip() for channel in extract.group(1).split(",")]
            new_channels = []
            for tc in channels_extract:
                if tc not in authorized_channels:
                    authorized_channels.append(tc)
                    new_channels.append(tc)
            if new_channels:
                new_channels_str = ", ".join(new_channels)
                await ctx.send(f"Added authorized channels: {new_channels_str}")
            else:
                await ctx.send("No new channels added. All channels have been authorized already.")
        else:
            if authorized_channels:
                await ctx.send(f"No new channels added. \nChannels: {', '.join(f'[{ch_name}]' for ch_name in authorized_channels)}")
            else:
                await ctx.send(f"No new channels added. \nUse format: `]channels <channel1>, <channel2>, ...`")

    """
    Function to submit feedback on songs (like/dislike)
    """
    @bot.command(name="feedback", help="Submit feedback for a song (like/dislike)")
    async def feedback(ctx, *, song_with_feedback: str):
        parts = song_with_feedback.rsplit(' ', 1)  # Split only at the last space
        if len(parts) != 2:
            await ctx.send("Invalid format. Use the format: ]feedback <song name> <like/dislike>")
            return
        
        song_name = parts[0]
        feedback_type = parts[1].strip().lower()
    
        print(f"Received feedback for song: {song_name}, Feedback Type: {feedback_type}")  # Debug line
    
        # Check for valid feedback
        if feedback_type not in ['like', 'dislike']:
            await ctx.send("Invalid feedback type. Please use 'like' or 'dislike'.")
            return
        
        # Get the queue (assuming a global instance of Songs_Queue)
        queue = Songs_Queue()
        queue.add_feedback(song_name, feedback_type)  # Adding feedback

        await ctx.send(f"Feedback '{feedback_type}' for '{song_name}' submitted successfully!")

        # Optionally, recommend a new song based on the feedback
        recommended_songs = recommend([])  # You can replace the empty list with context-specific songs
        await ctx.send(f"Here are some new recommendations: {', '.join(recommended_songs)}")

    """
    Function that is executed once any message is received by the bot
    """
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if message.channel.name in authorized_channels or message.channel.name == 'testing-space':
            await bot.process_commands(message)

    """
    Error checking function that returns any error received by the bot
    """
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, CheckFailure):
            await ctx.send("You need the DJ role to use this command!")
        else:
            print(f"An error has occurred: {error}")

    """
    Function to reconnect the bot to the VC 
    """
    @bot.command(name="reconnect", help="To connect the bot to voice channel")
    @has_role_dj()
    async def reconnect(ctx):
        await ctx.send("Reconnecting Enigma to VC ...")
        await on_ready()

    return bot  # Ensure to return the bot instance


# Create the bot instance
client = setup_bot()

if __name__ == '__main__':
    if client:  # Ensure client is not None 
        client.run(TOKEN)
    else:
        print("Failed to create the bot client.")
