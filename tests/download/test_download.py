# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import hashlib
import os
from pathlib import Path
import tempfile
from unittest.mock import call, patch, MagicMock

import aiohttp
import pytest

from download.core import download_file_async


@pytest.mark.asyncio
@patch("download.core.logger")
@patch("download.core.show_progress")
async def test_download(
    mock_show_progress: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:
    """Test a valid download"""

    # Setup
    url: str = "https://proof.ovh.net/files/1Mb.dat"
    mock_show_progress.return_value = None # No print

    with tempfile.TemporaryDirectory() as download_temp:
        file_path: Path = Path(download_temp) / "data.dat"
        await download_file_async(url, file_path)

        # Assertions request
        assert os.path.getsize(file_path) == 1048576, "Invalid size"
        with open(file_path, "rb") as f:
            assert hashlib.md5(f.read()).hexdigest() == "d5eefcccdb834958512bed157d01f3a7", \
                "Invalid md5 hash"

    # Assertions logs
    mock_log.info.assert_has_calls([
        call("Downloading %s to %s", url, file_path),
        call("Download done"),
    ])
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.core.logger")
@patch("download.core.show_progress")
async def test_download_invalid_url(
    mock_show_progress: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:
    """Test a download using an invalid url"""

    # Setup
    url: str = "https:////proof.ovh.net/files/1Mb.dat"
    mock_show_progress.return_value = None # No print

    with tempfile.TemporaryDirectory() as download_temp:
        file_path: Path = Path(download_temp) / "data.dat"

        # Assertion exception
        with pytest.raises(aiohttp.InvalidURL):
            await download_file_async(url, file_path)

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_has_calls([
        call("Connection error from %s", url),
    ])
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.core.logger")
@patch("download.core.show_progress")
async def test_download_client_connection_error(
    mock_show_progress: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:
    """Test a download using a valid url but from an nonexistent domaine"""

    # Setup
    url: str = "https://proof.ovh.error/files/1Mb.dat"
    mock_show_progress.return_value = None # No print

    with tempfile.TemporaryDirectory() as download_temp:
        file_path: Path = Path(download_temp) / "data.dat"

        # Assertion exception
        with pytest.raises(aiohttp.ClientConnectionError):
            await download_file_async(url, file_path)

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_has_calls([
        call("Connection error from %s", url),
    ])
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.core.logger")
@patch("download.core.show_progress")
async def test_download_client_response_error(
    mock_show_progress: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:
    """Test a download using a valid url but for an nonexistent page"""

    # Setup
    url: str = "https://proof.ovh.net/files/invalid"
    mock_show_progress.return_value = None # No print

    with tempfile.TemporaryDirectory() as download_temp:
        file_path: Path = Path(download_temp) / "data.dat"

        # Assertion exception
        with pytest.raises(aiohttp.ClientResponseError):
            await download_file_async(url, file_path)

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_has_calls([
        call("Invalid response from %s", url),
    ])
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.core.logger")
@patch("download.core.show_progress")
async def test_download_invalid_path(
    mock_show_progress: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:
    """Test to download in a non existent folder"""

    # Setup
    url: str = "https://proof.ovh.net/files/1Mb.dat"
    file_path: Path = Path("/do/not/exist") / "data.dat"
    mock_show_progress.return_value = None # No print

        # Assertion exception
    with pytest.raises(FileNotFoundError) :
        await download_file_async(url, file_path)

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_has_calls([
        call("Invalid path %s", file_path),
    ])
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()
