# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
from pathlib import Path
from unittest.mock import call, patch

import pytest

from download.core import moving_folder, moving_folder_async


@patch("download.core.logger")
def test_moving_folder_success(
    setup_folders,
    mock_log,
    mock_bot):

    """Test successfully moving a folder"""
    # Get the source and destination folders
    src_folder, dst_folder = setup_folders
    src_folder, dst_folder = Path(src_folder), Path(dst_folder)
    # Call the moving_folder function
    moving_folder(src_folder, dst_folder)

    # Check if the folder has been moved
    assert os.path.exists(dst_folder), "Source folder was not moved to the destination folder"

    # Check if the file is in the destination folder
    moved_file_path = Path(dst_folder) / "test.txt"
    assert os.path.exists(moved_file_path), "File was not moved to the destination folder"

    # Check the content of the moved file
    with open(moved_file_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "This is a test file.", "Content of the moved file is incorrect"

    # Assertions logs
    mock_log.info.assert_has_calls([
        call("Moving file from %s to %s", src_folder, dst_folder),
        call("Move file done")
    ])
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@patch("download.core.logger")
def test_moving_folder_src_not_exist(
    tmpdir,
    mock_log,
    mock_bot):

    """Test moving a nonexistent folder"""
    # Set up paths where the source folder doesn't exist
    src_folder = tmpdir / "non_existent_folder"
    dst_folder = tmpdir / "dst_folder"

    # Ensure destination folder exists
    os.makedirs(dst_folder, exist_ok=True)

    # Call the moving_folder function and expect a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        moving_folder(Path(src_folder), Path(dst_folder))

    # Assertions logs
    mock_log.info.assert_has_calls([
        call("Moving file from %s to %s", src_folder, dst_folder)
    ])
    mock_log.error.assert_has_calls([
        call("%s and/or %s does not exist", src_folder, dst_folder)
    ])
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.core.moving_folder", return_value=None)
async def test_moving_folder_async_success(
    mock_moving_folder,
    setup_folders,
    mock_log,
    mock_bot):

    """Test successfully moving a folder"""
    # Get the source and destination folders
    src_folder, dst_folder = setup_folders
    src_folder, dst_folder = Path(src_folder), Path(dst_folder)
    # Call the moving_folder function
    result = await moving_folder_async(mock_log, src_folder, dst_folder)

    # Assertions return
    assert result is None, "Moving folder should succeed"

    # Assertions subfunction
    mock_moving_folder.assert_has_calls([
        call(mock_log, src_folder, dst_folder)
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
@patch("download.core.moving_folder", side_effect=Exception("Moving folder failure"))
async def test_moving_folder_async_failure(
    mock_moving_folder,
    tmpdir,
    mock_log,
    mock_bot):

    """Test moving a nonexistent folder"""
    # Set up paths where the source folder doesn't exist
    src_folder = tmpdir / "non_existent_folder"
    dst_folder = tmpdir / "dst_folder"

    # Ensure destination folder exists
    os.makedirs(dst_folder, exist_ok=True)

    with pytest.raises(Exception):
        await moving_folder_async(src_folder, dst_folder)

    # Assertions subfunction
    mock_moving_folder.assert_has_calls([
        call(src_folder, dst_folder)
    ])

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()
