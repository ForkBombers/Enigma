"""
This file is responsible for all the helper functions that are used
"""
from youtubesearchpython import VideosSearch
from src.get_all import filtered_songs
from youtube_search import YoutubeSearch

import discord
from discord.ext import commands
from discord.ext.commands import CheckFailure

vc_connected = False  # global flag variable for vc connection status
"""
This function seaches the song on youtube and returns the URL
"""
# def searchSong(name_song):
#     videosSearch = VideosSearch(name_song, limit=1)
#     result = videosSearch.result()
#     link = result['result'][0]['link']
#     return link


def searchSong(name_song):
    videosSearch = YoutubeSearch(name_song, max_results=5).to_dict()
    result = videosSearch.result()
    link = result['result'][0]['link']
    return link


all_songs = filtered_songs()[["track_name", "artist", "genre"]]
"""
This function returns random 25 songs for generating the poll for the user
"""


def random_25():
    random_songs = (all_songs.sample(
        frac=1).groupby('genre').head(1)).sample(25)
    return random_songs


"""
Function to check if user had 'DJ' role
"""


def has_role_dj():

    async def predicate(ctx):
        dj_role = discord.utils.get(ctx.guild.roles, name='DJ')
        if dj_role in ctx.author.roles:
            return True
        raise CheckFailure("You do not have permission to use the bot")

    return commands.check(predicate)


async def update_vc_status(client, member, before, after):
    if member == client.user:
        # check if bot is disconnected
        if before.channel is not None and after.channel is None:
            vc_connected = False
            print(
                f"{str(member.name)} disconnected from {before.channel.name}")
        # check if bot is connected
        elif before.channel is None and after.channel is not None:
            vc_connected = True
            print(
                f"{str(member.name)} is online and connected to {after.channel.name}"
            )
        # attempt to reconnect bot
        else:
            voice_channel = discord.utils.get(client.voice_clients,
                                              guild=before.channel.guild)
            if voice_channel and not voice_channel.is_connected():
                await voice_channel.connect(reconnect=True, timeout=20.0)


def check_vc_status():

    def predicate(ctx):
        # global vc_connected
        if not vc_connected:
            raise commands.CheckFailure("Enigma is not connected to VC")
        return True

    return commands.check(predicate)
