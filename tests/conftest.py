# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from unittest.mock import AsyncMock, MagicMock

import pytest

pytest_plugins = ['pytest_asyncio']

@pytest.fixture
def mock_log() -> MagicMock:
    return MagicMock()

@pytest.fixture
def mock_bot() -> MagicMock:
    bot = MagicMock()
    bot.update_lock = AsyncMock()
    bot.update_lock.__aenter__.return_value = bot.update_lock
    bot.update_lock.__aexit__.return_value = None
    return bot
