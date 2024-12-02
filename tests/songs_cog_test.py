import pytest
import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from Cogs.songs_cog import *
from Cogs.songs_cog import Songs
import warnings
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.append("../")

warnings.filterwarnings("ignore")


@pytest.mark.asyncio
class Test_Songs_Cog(unittest.TestCase):

    async def test_resume(self):
        result = await Songs.resume()
        assert result == "The bot was not playing anything before this. Use play command"

    async def test_stop(self):
        result = await Songs.stop()
        assert result == "The bot is not playing anything at the moment."

    async def test_play_song(self):
        result = await Songs.play_song()
        assert result == "The bot is not connected to a voice channel."

    async def test_handle_empty_queue(self):
        result = await Songs.handle_empty_queue()
        assert result == "No recommendations present. First generate recommendations using /poll"

    async def test_pause(self):
        result = await Songs.pause()
        assert result == "The bot is not playing anything at the moment."

    async def test_shuffle(self):
        result = await Songs.shuffle()
        assert result == "Playlist shuffled"

    async def test_add_song(self):
        result = await Songs.add_song()
        assert result == "Song added to queue"

    async def test_queue(self):
        result = await Songs.queue()
        assert result == "No recommendations present. First generate recommendations using ]poll"

    async def test_next_song(self):
        result = await Songs.next_song()
        assert result == "The queue is empty."

    async def test_jump_to(self):
        result = await Songs.jump_to(song_name="Test Song")
        assert result == "No recommendations present. First generate recommendations using ]poll"


# @pytest.mark.asyncio
# async def test_play_song_youtube_link(songs_cog):
#     ctx_mock = AsyncMock()
#     ctx_mock.message.guild.voice_client = MagicMock()
#     ctx_mock.message.guild.voice_client.is_playing.return_value = False

#     # Mocking yt_dlp
#     with patch('yt_dlp.YoutubeDL.extract_info') as mock_extract:
#         mock_extract.return_value = {"url": "test_url", "title": "test_title"}

#         await songs_cog.play_song(ctx_mock,
#                                   "https://youtube.com/watch?v=test123")

#         mock_extract.assert_called_once()
#         ctx_mock.send.assert_called_with("Now playing: test_title")

@pytest.mark.asyncio
async def test_play_song_youtube_link(songs_cog):
    ctx_mock = AsyncMock()
    ctx_mock.message.guild.voice_client = MagicMock()
    ctx_mock.message.guild.voice_client.is_playing.return_value = False

    with patch('yt_dlp.YoutubeDL') as mock_ytdl:
        mock_ytdl.return_value.extract_info.return_value = {"url": "test_url", "title": "test_title"}
        
        # Mock asyncio.get_event_loop()
        with patch('asyncio.get_event_loop') as mock_get_loop:
            mock_loop = AsyncMock()
            mock_get_loop.return_value = mock_loop
            mock_loop.run_in_executor.return_value = mock_ytdl.return_value.extract_info.return_value

            await songs_cog.play_song(ctx_mock, "https://youtube.com/watch?v=test123")

    ctx_mock.send.assert_called_with("Now playing: test_title")

# @pytest.fixture
# def songs_cog():
#     bot_mock = MagicMock()
#     return Songs(bot_mock)

@pytest.fixture
def songs_cog():
    bot_mock = MagicMock()
    songs = Songs(bot_mock)
    songs.songs_queue = Songs_Queue([])
    #songs.queue = []  # Initialize an empty queue for tests
    return songs


# @pytest.mark.asyncio
# async def test_next_song_empty_queue(songs_cog):
#     songs_cog.songs_queue.queue = []
#     ctx_mock = AsyncMock()

#     await songs_cog.next_song.callback(songs_cog, ctx_mock)

#     assert ctx_mock.send.call_count == 2
#     calls = ctx_mock.send.call_args_list
#     assert "No recommendations present. First generate recommendations using ]poll" in calls[
#         0][0][0]
#     assert "The queue is empty." in calls[1][0][0]

@pytest.mark.asyncio
async def test_next_song_empty_queue(songs_cog):
    songs_cog.songs_queue.queue = []
    ctx_mock = AsyncMock()

    await songs_cog.next_song(songs_cog, ctx_mock)

    assert ctx_mock.send.call_count == 1
    calls = ctx_mock.send.call_args_list
    assert "No recommendations present" in calls[0][0][0]
    #assert "No more songs in the queue" in calls[1][0][0]

@pytest.mark.asyncio
async def test_play_not_connected(songs_cog):
    ctx_mock = AsyncMock()
    ctx_mock.message.guild.voice_client = None

    # Directly call the method, passing ctx_mock as the first argument
    await songs_cog.play.callback(songs_cog, ctx_mock)

    ctx_mock.send.assert_called_once()
    assert "The bot is not connected to any voice channel" in ctx_mock.send.call_args[
        0][0]

@pytest.mark.asyncio
async def test_jump_to_empty_queue(songs_cog):
    songs_cog.songs_queue.queue = []
    ctx_mock = AsyncMock()

    # Directly call the method, passing ctx_mock as the first argument
    await songs_cog.jump_to.callback(songs_cog,
                                     ctx_mock,
                                     song_name="Test Song")

    ctx_mock.send.assert_called_once()
    assert "No recommendations present" in ctx_mock.send.call_args[0][0]


@pytest.mark.asyncio
async def test_jump_empty_queue(songs_cog):
    ctx_mock = AsyncMock()
    ctx_mock.message.guild.voice_client = MagicMock()
    ctx_mock.message.guild.voice_client.is_connected.return_value = True

    # Set an empty queue
    songs_cog.songs_queue = Songs_Queue([])

    # Access the command's callback
    await songs_cog.jump_to.callback(songs_cog,
                                     ctx_mock,
                                     song_name="some_song")

    ctx_mock.send.assert_called_with(
        "No recommendations present. First generate recommendations using ]poll"
    )
    assert songs_cog.songs_queue.get_len() == 0  # Check if the queue is empty
    assert songs_cog.songs_queue.queue == [
    ]  # Check if the internal queue list is empty


@pytest.mark.asyncio
async def test_jump_non_numeric_position(songs_cog):
    ctx_mock = AsyncMock()
    ctx_mock.message.guild.voice_client = MagicMock()
    ctx_mock.message.guild.voice_client.is_connected.return_value = True

    songs_cog.songs_queue = Songs_Queue(["song1", "song2", "song3", "song4"])

    await songs_cog.jump_to.callback(songs_cog, ctx_mock,
                                     song_name="abc")  # Non-numeric input
    ctx_mock.send.assert_called_with("Song 'abc' not found in the queue.")


# @pytest.mark.asyncio
# async def test_jump_to_current_song(songs_cog):
#     ctx_mock = AsyncMock()
#     ctx_mock.message.guild.voice_client = MagicMock()
#     ctx_mock.message.guild.voice_client.is_connected.return_value = True

#     songs_cog.songs_queue = Songs_Queue(["song1", "song2", "song3", "song4"])

#     await songs_cog.jump_to.callback(songs_cog, ctx_mock, song_name="song1")  # Jump to the first song
#     ctx_mock.send.assert_called_with("Now playing: SEREBRO - Song #1 [Original Version]")


@pytest.mark.asyncio
async def test_jump_to_invalid_position(songs_cog):
    ctx_mock = AsyncMock()
    ctx_mock.message.guild.voice_client = MagicMock()
    ctx_mock.message.guild.voice_client.is_connected.return_value = True

    songs_cog.songs_queue = Songs_Queue(["song1", "song2", "song3", "song4"])

    await songs_cog.jump_to.callback(songs_cog,
                                     ctx_mock,
                                     song_name="invalid_song")  # Invalid index
    ctx_mock.send.assert_called_with(
        "Song 'invalid_song' not found in the queue.")
