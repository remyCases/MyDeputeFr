# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
from pathlib import Path
from typing import Tuple
from unittest.mock import call, patch, MagicMock
import zipfile

import pytest

from download.core import unzip_file, unzip_file_async


@patch("download.core.logger")
def test_unzip_file_success(
        mock_log: MagicMock,
        valid_zip: Tuple[Path, Path],
        mock_bot: MagicMock) -> None:

    """Test a correct unzipping"""
    # Get the zip file path and destination folder
    zip_path, dst_folder = valid_zip

    # Ensure destination folder exists
    os.makedirs(dst_folder, exist_ok=True)

    # Call the unzip function
    unzip_file(zip_path, dst_folder)

    # Check if the file has been extracted
    extracted_file_path: Path = dst_folder / "test.txt"
    assert os.path.exists(extracted_file_path), "Extracted file not found in destination folder"

    # Check the content of the extracted file
    with open(extracted_file_path, "r", encoding="utf-8") as f:
        content: str = f.read()
    assert content == "This is a test file.", "Content of extracted file is incorrect"

    # Assertions logs
    mock_log.info.assert_has_calls([
        call("Unzipping file %s to %s", zip_path, dst_folder),
        call("Unzip done"),
    ])
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@patch("download.core.logger")
def test_unzip_file_bad_zip(
        mock_log: MagicMock,
        tmp_path: Path,
        mock_bot: MagicMock) -> None:

    """Test unzipping an invalid file"""
    # Create an invalid zip file (not actually a zip file)
    bad_zip_path: Path = tmp_path / "bad.zip"
    with open(bad_zip_path, "w", encoding="utf-8") as f:
        f.write("This is not a zip file.")

        # Call the unzip function and expect it to raise an exception
        with pytest.raises(zipfile.BadZipFile):
            unzip_file(bad_zip_path, tmp_path)

    # Assertions logs
    mock_log.info.assert_has_calls([
        call("Unzipping file %s to %s", bad_zip_path, tmp_path),
    ])
    mock_log.error.assert_has_calls([
        call("%s is not a correct Zip File.", bad_zip_path)
    ])
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@patch("download.core.logger")
def test_unzip_file_file_not_found(
    mock_log: MagicMock,
    tmp_path: Path,
    mock_bot: MagicMock) -> None:

    """Test unzipping an non existent file"""
    # Simulate a FileNotFoundError by providing a non-existent file path
    non_existent_zip_path: Path = tmp_path / "non_existent.zip"

    # Call the unzip function and expect it to raise an exception
    with pytest.raises(FileNotFoundError):
        unzip_file(non_existent_zip_path, tmp_path)

    # Assertions logs
    mock_log.info.assert_has_calls([
        call("Unzipping file %s to %s", non_existent_zip_path, tmp_path),
    ])
    mock_log.error.assert_has_calls([
        call("%s does not exist.", non_existent_zip_path)
    ])
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.core.logger")
@patch("download.core.unzip_file", return_value=None)
async def test_unzip_file_async_success(
    mock_unzip_file: MagicMock,
    mock_log: MagicMock,
    valid_zip: Tuple[Path, Path],
    mock_bot: MagicMock) -> None:

    """Test a correct unzipping"""
    # Get the zip file path and destination folder
    zip_path, dst_folder = valid_zip

    # Call the unzip function
    await unzip_file_async(zip_path, dst_folder)

    # Assertions subfunctions
    mock_unzip_file.assert_has_calls([
        call(zip_path, dst_folder)
    ])

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.core.logger")
@patch("download.core.unzip_file", side_effect=Exception("Unzip failure"))
async def test_unzip_file_async_failure(
    mock_unzip_file: MagicMock,
    mock_log: MagicMock,
    tmp_path: Path,
    mock_bot: MagicMock) -> None:

    """Test unzipping an invalid file"""
    # Create an invalid zip file (not actually a zip file)
    bad_zip_path: Path = tmp_path / "bad.zip"
    with open(bad_zip_path, "w", encoding="utf-8") as f:
        f.write("This is not a zip file.")

    # Call the unzip function and expect it to raise an exception
    with pytest.raises(Exception):
        await unzip_file_async(bad_zip_path, tmp_path)

    # Assertions subfunctions
    mock_unzip_file.assert_has_calls([
        call(bad_zip_path, tmp_path)
    ])

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()
