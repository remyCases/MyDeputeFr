from unittest.mock import AsyncMock, MagicMock, patch, mock_open

import discord
import pytest
from discord.ext.commands import Context

from cogs.deputeCommand import DeputeCommand
from tests.conftest import mock_bot

@pytest.fixture
def mock_context():
    ctx = MagicMock(spec=Context)
    ctx.send = AsyncMock()
    ctx.bot = MagicMock()
    ctx.bot.mode = "DEBUG"
    return ctx


# TODO
