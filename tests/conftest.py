# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from unittest.mock import MagicMock

import pytest


@pytest.fixture(scope="session")
def mock_log():
    return MagicMock()

@pytest.fixture(scope="session")
def mock_bot():
    return MagicMock()
