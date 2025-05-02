# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
from pathlib import Path
from unittest.mock import call, patch
import zipfile

import pytest

from download.core import unzip_file, unzip_file_async


@patch("download.core.logger")
def test_unzip_file_success(
        valid_zip,
        mock_log,
        mock_bot):

    """Test a correct unzipping"""
    # Get the zip file path and destination folder
    zip_path, dst_folder = valid_zip

    # Ensure destination folder exists
    os.makedirs(dst_folder, exist_ok=True)

    # Call the unzip function
    unzip_file(zip_path, dst_folder)

    # Check if the file has been extracted
    extracted_file_path = dst_folder / "test.txt"
    assert os.path.exists(extracted_file_path), "Extracted file not found in destination folder"

    # Check the content of the extracted file
    with open(extracted_file_path, "r", encoding="utf-8") as f:
        content = f.read()
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
        tmpdir,
        mock_log,
        mock_bot):

    """Test unzipping an invalid file"""
    # Create an invalid zip file (not actually a zip file)
    bad_zip_path = tmpdir / "bad.zip"
    with open(bad_zip_path, "w", encoding="utf-8") as f:
        f.write("This is not a zip file.")

        # Call the unzip function and expect it to raise an exception
        with pytest.raises(zipfile.BadZipFile):
            unzip_file(Path(bad_zip_path), Path(tmpdir))

    # Assertions logs
    mock_log.info.assert_has_calls([
        call("Unzipping file %s to %s", Path(bad_zip_path), Path(tmpdir)),
    ])
    mock_log.error.assert_has_calls([
        call("%s is not a correct Zip File.", Path(bad_zip_path))
    ])
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


def test_unzip_file_file_not_found(
    tmpdir,
    mock_log,
    mock_bot):

    """Test unzipping an non existent file"""
    # Simulate a FileNotFoundError by providing a non-existent file path
    non_existent_zip_path = tmpdir / "non_existent.zip"

    # Call the unzip function and expect it to raise an exception
    with pytest.raises(FileNotFoundError):
        unzip_file(Path(non_existent_zip_path), Path(tmpdir))

    # Assertions logs
    mock_log.info.assert_has_calls([
        call("Unzipping file %s to %s", Path(non_existent_zip_path), Path(tmpdir)),
    ])
    mock_log.error.assert_has_calls([
        call("%s does not exist.", Path(non_existent_zip_path))
    ])
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.core.unzip_file", return_value=None)
async def test_unzip_file_async_success(
    mock_unzip_file,
    valid_zip,
    mock_log,
    mock_bot):

    """Test a correct unzipping"""
    # Get the zip file path and destination folder
    zip_path, dst_folder = valid_zip

    # Call the unzip function
    result = await unzip_file_async(zip_path, dst_folder)

    # Assertions return
    assert result is None, "unzip should success"

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
@patch("download.core.unzip_file", side_effect=Exception("Unzip failure"))
async def test_unzip_file_async_failure(
    mock_unzip_file,
    tmpdir,
    mock_log,
    mock_bot):

    """Test unzipping an invalid file"""
    # Create an invalid zip file (not actually a zip file)
    bad_zip_path: Path = tmpdir / "bad.zip"
    with open(bad_zip_path, "w", encoding="utf-8") as f:
        f.write("This is not a zip file.")

    # Call the unzip function and expect it to raise an exception
    with pytest.raises(Exception):
        await unzip_file_async(bad_zip_path, tmpdir)

    # Assertions subfunctions
    mock_unzip_file.assert_has_calls([
        call(bad_zip_path, tmpdir)
    ])

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()
