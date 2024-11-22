import unittest
from unittest.mock import patch, MagicMock
import discord
from discord.ext import commands
from src.utils import searchSong, random_25, has_role_dj, update_vc_status, check_vc_status


class TestUtils(unittest.TestCase):

    def test_random_25(self):
        random_songs = random_25()
        self.assertTrue(len(random_songs) == 25)

    @patch('discord.utils.get')
    async def test_has_role_dj(self, mock_get):
        # Mock the discord context and role
        ctx = MagicMock()
        ctx.guild.roles = ["DJ", "User"]
        ctx.author.roles = ["DJ"]

        mock_get.return_value = "DJ"

        # Create a dummy command
        @commands.command()
        @has_role_dj()
        async def dummy_command(ctx):
            pass

        # Test if the command runs without raising an exception
        try:
            await dummy_command(ctx)
        except commands.CheckFailure:
            self.fail("has_role_dj() raised CheckFailure unexpectedly!")

    @patch('discord.utils.get')
    async def test_update_vc_status(self, mock_get):
        client = MagicMock()
        member = MagicMock()
        before = MagicMock()
        after = MagicMock()

        # Test bot disconnection
        before.channel = MagicMock()
        after.channel = None
        await update_vc_status(client, member, before, after)
        self.assertFalse(vc_connected)

        # Test bot connection
        before.channel = None
        after.channel = MagicMock()
        await update_vc_status(client, member, before, after)
        self.assertTrue(vc_connected)

    def test_check_vc_status(self):
        global vc_connected

        # Test when vc is connected
        vc_connected = True

        @commands.command()
        @check_vc_status()
        async def dummy_command(ctx):
            pass

        ctx = MagicMock()
        self.assertTrue(check_vc_status().predicate(ctx))


if __name__ == '__main__':
    unittest.main()
