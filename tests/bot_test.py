import unittest
from unittest.mock import AsyncMock, patch
import sys
import re
from discord.ext.commands import CheckFailure

sys.path.append("../")
from bot import client, authorized_channels


class TestDiscordBot(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.guild = AsyncMock()
        self.channel = AsyncMock()
        self.channel.name = "testing-space"
        self.member = AsyncMock()
        self.member.roles = []

    @patch("bot.client.get_channel")
    async def test_on_ready(self, mock_get_channel):
        # Mock voice channel and simulate bot connecting
        mock_voice_channel = AsyncMock()
        mock_get_channel.return_value = mock_voice_channel
        await client.on_ready()
        mock_voice_channel.connect.assert_called_once()

    async def test_on_voice_state_update_reconnect(self):
        # Test reconnect behavior when bot disconnects from a voice channel
        before = AsyncMock(channel=AsyncMock(name="Voice Channel"))
        after = AsyncMock(channel=None)
        await client.on_voice_state_update(self.member, before, after)
        # Here, assert that reconnect logic was called correctly as per ⁠ update_vc_status ⁠ handling.

    async def test_on_message(self):
        # Test message handling in authorized and unauthorized channels
        message = AsyncMock()
        message.author = AsyncMock()
        message.author == client.user  # Avoid bot processing its own messages
        message.channel.name = "testing-space"
        await client.on_message(message)
        # Verify if ⁠ process_commands ⁠ was called in an authorized channel

        message.channel.name = "unauthorized-channel"
        await client.on_message(message)
        # Ensure that commands are ignored in unauthorized channels

    async def test_on_command_error(self):
        # Simulate a command error for CheckFailure (missing DJ role)
        ctx = AsyncMock()
        error = CheckFailure("DJ role required")
        ctx.send = AsyncMock()

        await client.on_command_error(ctx, error)
        ctx.send.assert_called_once_with(
            "You need the DJ role to use this command!")


if __name__ == "_main_":
    unittest.main()
