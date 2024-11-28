"""
This file is responsible for all bot commands regarding songs such ]poll for generating recommendations,
]next_song for playing next song and so on
"""

import discord
from dotenv import load_dotenv
from discord.ext import commands
#import youtube_dl
import yt_dlp
import asyncio
import sys
import urllib.parse, urllib.request, re
from collections import defaultdict

from src.get_all import *
from src.utils import searchSong, random_25, has_role_dj, check_vc_status
from src.songs_queue import Songs_Queue

# client = commands.Bot(command_prefix=']', intents=intents)
# client.add_check(check_vc_status)

FFMPEG_OPTIONS = {
    "before_options":
    "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": [
        "ffmpeg",
        "-i",
        "./assets/sample.mp4",
        "-vn",
        "-f",
        "mp3",
        "./assets/sample.mp3",
    ],
}

ffmpeg_options = {
    'before_options':
    '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -filter:a "volume=0.25"'
}

youtube_base_url = 'https://www.youtube.com/'
youtube_results_url = youtube_base_url + 'results?'
youtube_watch_url = youtube_base_url + 'watch?v='
YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'True'}
ytdl = yt_dlp.YoutubeDL(YDL_OPTIONS)
# self.songs_queue = []


class Songs(commands.Cog):
    """
    Cog for bot that handles all commands related to songs
    """

    def __init__(self, bot):
        self.bot = bot
        self.songs_queue = Songs_Queue([])
        self.user_feedback = defaultdict(lambda: {
            'liked': [],
            'disliked': []
        })  # Stores feedback for users

    # """
    # Function for playing a song
    # """
    # @commands.command(name='play', help='To play a song')
    # @has_role_dj()
    # async def play(self, ctx):
    #     # await ctx.send(f"Playing {song} requested by {ctx.author.display_name}")
    #     user_message = str(ctx.message.content)
    #     song_name = user_message.split(' ', 1)[1]
    #     await self.play_song(song_name, ctx)
    """
    Function to resume playing
    """

    @commands.command(name="resume", help="Resumes the song")
    @has_role_dj()
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client is None:

            await ctx.send(
                "The bot is not connected to any voice channel at the moment.")

        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send(
                "The bot was not playing anything before this. Use play command"
            )

    """
    Function for playing a custom song
    """

    @commands.command(name="play_custom", help="To play custom song")
    @has_role_dj()
    async def play_custom(self, ctx):
        voice_client = ctx.message.guild.voice_client
        user_message = str(ctx.message.content)
        song_name = user_message.split(' ', 1)[1]
        if voice_client.is_playing():
            voice_client.pause()
            await self.play_song(ctx, song_name=song_name)
            return  #

        # await self.play_song(ctx, song_name=song_name)

    """
    Function to stop playing the music
    """

    @commands.command(name="stop", help="Stops the song")
    @has_role_dj()
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    async def play_song(self, ctx, song_name):
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client

            # Check if the bot is connected to a voice channel
            if not voice_channel:
                await ctx.send("The bot is not connected to any voice channel."
                               )
                return

            # Stop any currently playing audio before starting a new one
            if voice_channel.is_playing():
                voice_channel.stop()

            # Check if song_name is a YouTube URL; otherwise, perform a search
            if youtube_base_url not in song_name:
                query_string = urllib.parse.urlencode(
                    {'search_query': song_name})
                content = urllib.request.urlopen(youtube_results_url +
                                                 query_string)
                search_results = re.findall(r'/watch\?v=(.{11})',
                                            content.read().decode())
                if not search_results:
                    await ctx.send("No results found for the song.")
                    return

                link = youtube_watch_url + search_results[0]
            else:
                link = song_name  # song_name is already a URL

            # Fetch video data asynchronously
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(
                None, lambda: ytdl.extract_info(link, download=False))

            # Validate the retrieved song URL
            if 'url' not in data:
                await ctx.send("Unable to retrieve the song URL.")
                return

            song = data['url']
            song_title = data['title']
            await ctx.send(f"Now playing: {song_title}")
            print(f"Now playing: {song_title}")

            # Play the audio
            player = discord.FFmpegOpusAudio(song, **ffmpeg_options)
            voice_channel.play(player)

            # After successfully playing the song, update the current_index
            self.songs_queue.current_index = self.songs_queue.index
            self.songs_queue.save_to_json()

        except Exception as e:
            # Generic error handling, providing a more detailed message
            await ctx.send(
                f"An error occurred while trying to play the song: {str(e)}")
            print(f"Error in play_song(): {e}")

    """
    Function to loop the song or queue
    """

    @commands.command(name="loop", help="Toggle loop mode (off/song/queue)")
    @has_role_dj()
    async def loop(self, ctx):
        mode = self.songs_queue.toggle_loop()
        await ctx.send(f"Loop mode set to: {mode}")

    """
    Function to replay the current song
    """

    @commands.command(name="replay", help="Replay the current song")
    @has_role_dj()
    async def replay(self, ctx):
        current_song = self.songs_queue.replay_current()
        if current_song:
            await ctx.send(f"Replaying: {current_song}")
            await self.play_song(ctx, current_song)
        else:
            await ctx.send("No song to replay.")

    """
    Helper function to handle empty song queue
    """

    async def handle_empty_queue(self, ctx):
        if self.songs_queue.get_len() == 0:
            await ctx.send(
                "No recommendations present. First generate recommendations using ]poll"
            )
            return True
        return False

    """
    Function to play the next song in the queue
    """

    @commands.command(name="next_song", help="To play next song in queue")
    @has_role_dj()
    async def next_song(self, ctx):
        empty_queue = await self.handle_empty_queue(ctx)
        if empty_queue:
            return

        voice_client = ctx.message.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()

        next_song = self.songs_queue.next_song()
        if next_song is None:
            await ctx.send("No more songs in the queue")
            return

        await ctx.send(f"Playing the next song: {next_song}")
        await self.play_song(ctx, next_song)

    """
    Function to play the previous song in the queue
    """

    @commands.command(name="prev_song", help="To play prev song in queue")
    @has_role_dj()
    async def prev_song(self, ctx):
        empty_queue = await self.handle_empty_queue(ctx)
        if empty_queue:
            return

        voice_client = ctx.message.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()

        prev_song = self.songs_queue.prev_song()
        if prev_song is None:
            await ctx.send("No previous songs in the queue")
            return

        await ctx.send(f"Playing the previous song: {prev_song}")
        await self.play_song(ctx, prev_song)

    """
    Function to pause the song that is playing
    """

    @commands.command(name='pause', help='This command pauses the song')
    @has_role_dj()
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client is None:

            await ctx.send(
                "The bot is not connected to any voice channel at the moment.")
        elif voice_client.is_playing():
            await voice_client.pause()
            await ctx.send("The song is paused now.")
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    """
    Function to jump to a specific song within the queue
    """

    @commands.command(name="jump_to",
                      help="Jump to a specific song in the queue")
    @has_role_dj()
    async def jump_to(self, ctx, *, song_name: str):
        empty_queue = await self.handle_empty_queue(ctx)
        if empty_queue:
            return

        jumped_song = self.songs_queue.jump_to_song(song_name)

        if jumped_song is None:
            await ctx.send(f"Song '{song_name}' not found in the queue.")
            return

        # Stop the current song if it's playing
        voice_client = ctx.message.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()

        # Play the selected song
        await ctx.send(f"Jumping to: {jumped_song}")
        await self.play_song(ctx, jumped_song)

    """
    Like command to store feedback for songs
    """

    @commands.command(name="like",
                      help="Like a song to improve recommendations")
    async def like(self, ctx):
        current_song = self.songs_queue.current_song(
        )  # Get the currently playing song
        if not current_song:
            await ctx.send("No song is currently playing to like.")
            return

        # Save the feedback
        user_id = ctx.author.id
        if current_song not in self.user_feedback[user_id]['liked']:
            self.user_feedback[user_id]['liked'].append(current_song)
            # Optionally, provide feedback to user
            await ctx.send(f"Liked: {current_song}")

        # Adjust recommendations based on likes
        await self.adjust_recommendations(ctx)

    """
    Dislike command to store feedback for songs
    """

    @commands.command(name="dislike",
                      help="Dislike a song to avoid similar ones")
    async def dislike(self, ctx):
        current_song = self.songs_queue.current_song(
        )  # Get the currently playing song
        if not current_song:
            await ctx.send("No song is currently playing to dislike.")
            return

        # Save the feedback
        user_id = ctx.author.id
        if current_song not in self.user_feedback[user_id]['disliked']:
            self.user_feedback[user_id]['disliked'].append(current_song)
            # Optionally, provide feedback to user
            await ctx.send(f"Disliked: {current_song}")

        # Adjust recommendations based on dislikes
        await self.adjust_recommendations(ctx)

    """
    Function to adjust recommendations based on feedback
    """

    async def adjust_recommendations(self, ctx):
        # Collect liked and disliked songs from all users
        liked_songs = set()
        disliked_songs = set()

        # Collect user feedback
        for user_id, feedback in self.user_feedback.items():
            liked_songs.update(feedback['liked'])
            disliked_songs.update(feedback['disliked'])

        # Recommend songs based on feedback (excluding disliked and favoring liked)
        all_songs = random_25()  # Or use your existing recommendation function
        recommended_songs = [
            song for song in all_songs if song not in disliked_songs
        ]

        # You can fine-tune this to favor liked songs if necessary
        if liked_songs:
            recommended_songs = [
                song for song in all_songs if song in liked_songs
            ] + recommended_songs

        # Update the queue
        self.songs_queue = Songs_Queue(recommended_songs)

        # Play the next recommended song
        if recommended_songs:
            await self.play_song(ctx, self.songs_queue.next_song())
        else:
            await ctx.send("No more recommendations based on your feedback.")

    """
    Function to generate poll for playing the recommendations
    """

    @commands.command(name="poll", help="Poll for recommendation")
    # @has_role_dj()
    async def poll(self, ctx):

        # self.self.songs_queue = []
        reactions = ['👍', '👎']
        selected_songs = []
        count = 0
        bot_message = "Select song preferences by reaction '👍' or '👎' to the choices. \nSelect 3 songs"
        await ctx.send(bot_message)
        ten_random_songs = random_25()
        for ele in zip(ten_random_songs["track_name"],
                       ten_random_songs["artist"]):
            bot_message = str(ele[0]) + " By " + str(ele[1])
            description = []
            poll_embed = discord.Embed(title=bot_message,
                                       color=0x31FF00,
                                       description="".join(description))
            react_message = await ctx.send(embed=poll_embed)
            for reaction in reactions[:len(reactions)]:
                await react_message.add_reaction(reaction)
            res, user = await self.bot.wait_for("reaction_add")
            if res.emoji == "👍":
                selected_songs.append(str(ele[0]))
                count += 1
            if count == 3:
                bot_message = "Selected songs are : " + " , ".join(
                    selected_songs)
                await ctx.send(bot_message)
                break
        recommended_songs = recommend(selected_songs)
        self.songs_queue = Songs_Queue(recommended_songs)
        # print(self.songs_queue.next_song())
        await self.play_song(ctx, self.songs_queue.next_song())
        # await self.play_song(self.songs_queue.next_song(), ctx)

    """
    Function to display all the songs in the queue
    """

    @commands.command(name="queue",
                      help="Show active queue of recommendations")
    @has_role_dj()
    async def queue(self, ctx):
        empty_queue = await self.handle_empty_queue(ctx)
        if not empty_queue:
            queue, index = self.songs_queue.return_queue()
            await ctx.send("Queue of recommendations: ")
            # self.songs_queue = queue
            self.songs_queue.queue = queue
            for i in range(len(queue)):
                if i == index:
                    await ctx.send("Currently Playing: " + queue[i])
                else:
                    await ctx.send(queue[i])

    """
    Function to shuffle songs in the queue
    """

    @commands.command(name="shuffle", help="To shuffle songs in queue")
    @has_role_dj()
    async def shuffle(self, ctx):
        empty_queue = await self.handle_empty_queue(ctx)
        if not empty_queue:
            self.songs_queue.shuffle_queue()
            await ctx.send("Playlist shuffled")

    """
    Function to add custom song to the queue
    """

    @commands.command(name="add_song", help="To add custom song to the queue")
    @has_role_dj()
    async def add_song(self, ctx):
        user_message = str(ctx.message.content)
        song_name = user_message.split(" ", 1)[1]
        is_first_song = self.songs_queue.add_to_queue(song_name)
        await ctx.send("Song added to queue")

        if is_first_song:
            await ctx.send(f"Now playing: {song_name}")
            await self.play_song(ctx, song_name)

    """
    Recommending songs based on genre
    """

    @commands.command(name="genre",
                      help="To play 5 unique songs from the specified genre")
    async def play_song_genre(self, ctx, *, genre_name):
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client

            selected_songs = set()
            url_list = []

            ydl_opts = {
                'format': 'bestaudio/best',
                'noplaylist': True,
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                search_query = f"ytsearch5:{genre_name} music"
                info = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: ydl.extract_info(search_query, download=False))

                if 'entries' in info:
                    for entry in info['entries']:
                        if len(selected_songs) >= 5:
                            break
                        song_title = entry['title']
                        if song_title not in selected_songs:
                            selected_songs.add(song_title)
                            url_list.append(entry['webpage_url'])

            if len(selected_songs) < 5:
                await ctx.send(
                    f"Could only find {len(selected_songs)} unique songs for the genre '{genre_name}'."
                )

            await ctx.send("Playing songs:")
            for song in selected_songs:
                await ctx.send(song)

            self.songs_queue = Songs_Queue(list(selected_songs))

            # Start playing the first song
            if url_list:
                await self.play_song(ctx, self.songs_queue.next_song())

        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    """
    Function to play the current song from the queue
    """

    @commands.command(name='play', help="Resume playing from queue")
    @has_role_dj()
    async def play(self, ctx):
        voice_client = ctx.message.guild.voice_client
        user_message = str(ctx.message.content)  #
        match = re.search(r"\]play\s*(.+)", user_message)  #
        if match is None:
            song_name = ""
        else:
            song_name = match.group(1)  #
        # song_name = user_message.split(' ', 1)[1]
        if voice_client is None:
            await ctx.send("The bot is not connected to any voice channel.")
            return

        if song_name is None or song_name == "":
            try:
                index = self.songs_queue.current_index + 1
                # self.songs_queue.queue.index = index
                song_in_queue = self.songs_queue.queue[index]
                print(f"Index = {index} \nSong in Queue: {song_in_queue}")
                print(f"Playing next from queue: {song_in_queue}")
                await ctx.send(f"Playing next from queue: {song_in_queue}")
                await self.play_song(ctx, song_in_queue)
            except Exception as e:
                await ctx.send("There are no more songs in the queue")

        else:
            if voice_client.is_playing():
                voice_client.pause()
                await self.play_song(ctx, song_name=song_name)
                return

    """
    Function to move songs within the queue
    """

    @commands.command(name="move_song",
                      help="Move a song to a different position in the queue")
    @has_role_dj()
    async def move_song(self, ctx, from_pos: int, to_pos: int):
        empty_queue = await self.handle_empty_queue(ctx)
        if empty_queue:
            return

        # Adjust positions to be 0-indexed
        from_pos -= 1
        to_pos -= 1

        if self.songs_queue.move_song(from_pos, to_pos):
            await ctx.send(
                f"Moved song from position {from_pos + 1} to {to_pos + 1}")
            await self.display_queue(ctx)
        else:
            await ctx.send(
                "Invalid positions. Please check the queue and try again.")

    async def display_queue(self, ctx):
        queue, index = self.songs_queue.return_queue()
        queue_message = "Current Queue:\n"
        for i, song in enumerate(queue, start=1):
            if i - 1 == index:
                queue_message += f"**{i}. {song} (Currently Playing)**\n"
            else:
                queue_message += f"{i}. {song}\n"
        await ctx.send(queue_message)

    """
        Function to add the cog to the bot
    """


async def setup(client):
    await client.add_cog(Songs(client))
