# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.
import asyncio
from unittest.mock import MagicMock

import pytest

pytest_plugins = ['pytest_asyncio']

@pytest.fixture(scope="session")
def mock_log():
    return MagicMock()

@pytest.fixture(scope="session")
def mock_bot():
    mock_bot = MagicMock()
    mock_bot.bot.update_lock = MagicMock(spec=asyncio.Lock)
    mock_bot.bot.update_lock.locked.return_value = False
    mock_bot.bot.is_updating = False
    return mock_bot
