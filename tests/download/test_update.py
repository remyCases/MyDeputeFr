# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from config import config
from download.update import update_async

@pytest.mark.asyncio
@patch("download.update.logger")
@patch("download.update.moving_folder_async")
@patch("download.update.unzip_file_async")
@patch("download.update.download_file_async")
async def test_update_success(mock_download_file_async, mock_unzip_file_async, mock_moving_file_async, mock_log):
    # Setup
    mock_temp_dir_path = Path("/tmp_dir/")
    mock_temp_dir_context_manager = MagicMock()
    mock_temp_dir_context_manager.__enter__.return_value = mock_temp_dir_path
    mock_temp_dir = MagicMock(return_value=mock_temp_dir_context_manager)


    # Mock the functions used in the update process
    with (patch('tempfile.TemporaryDirectory', mock_temp_dir)):
        # Mock the behavior of each function to simulate success
        mock_download_file_async.return_value = None  # No error
        mock_unzip_file_async.return_value = None  # No error
        mock_moving_file_async.return_value = None  # No error

        # Call the update function
        result = await update_async()

        # Assertions
        assert result is True, "Update should succeed"
        mock_log.info.assert_any_call("=== Update starting ===")
        mock_log.info.assert_any_call("=== Update success ===")

        # Check that the functions were called correctly
        mock_download_file_async.assert_any_call(config.UPDATE_URL_DOWNLOAD_SCRUTINS,
                                                 Path("/tmp_dir/data_scrutins.zip"))
        mock_download_file_async.assert_any_call(config.UPDATE_URL_DOWNLOAD_ACTEUR_ORGANE,
                                                 Path("/tmp_dir/data_acteur_organe.zip"))
        mock_unzip_file_async.assert_any_call(Path("/tmp_dir/data_scrutins.zip"),
                                              Path("/tmp_dir/scrutins"))
        mock_unzip_file_async.assert_any_call(Path("/tmp_dir/data_acteur_organe.zip"),
                                              Path("/tmp_dir/acteur_organe"))
        mock_moving_file_async.assert_any_call(Path("/tmp_dir/scrutins/json"),
                                               config.SCRUTINS_FOLDER)
        mock_moving_file_async.assert_any_call(Path("/tmp_dir/acteur_organe/json/acteur"),
                                               config.ACTEUR_FOLDER)
        mock_moving_file_async.assert_any_call(Path("/tmp_dir/acteur_organe/json/organe"),
                                               config.ORGANE_FOLDER)

@pytest.mark.asyncio
@patch("download.update.logger")
@patch("download.update.download_file_async")
async def test_update_download_fail(mock_download_file_async, mock_log):
    # Mock download failure (download_file raises an exception)
    mock_download_file_async.side_effect = Exception("Download failed")

    # Call the update function
    result = await update_async()

    # Assertions
    assert result is False, "Update should fail due to download failure"
    mock_log.error.assert_any_call("Update failed : %s", "download failed")
    mock_log.error.assert_any_call("Error : %s", "Download failed")
    mock_log.error.assert_any_call("=== Update failed ===")

@pytest.mark.asyncio
@patch("download.update.logger")
@patch("download.update.unzip_file_async")
@patch("download.update.download_file_async")
async def test_update_unzip_fail(mock_download_file_async, mock_unzip_file_async, mock_log):
    # Mock download and unzip failure
    mock_download_file_async.return_value = None  # No error
    mock_unzip_file_async.side_effect = Exception("Unzip failed")

    # Call the update function
    result = await update_async()

    # Assertions
    assert result is False, "Update should fail due to unzip failure"
    mock_log.error.assert_any_call("Update failed : %s", "unzipping failed")
    mock_log.error.assert_any_call("Error : %s", "Unzip failed")
    mock_log.error.assert_any_call("=== Update failed ===")


@pytest.mark.asyncio
@patch("download.update.logger")
@patch("download.update.moving_folder_async")
@patch("download.update.unzip_file_async")
@patch("download.update.download_file_async")
async def test_update_move_fail(mock_download_file_async, mock_unzip_file_async, mock_moving_file_async, mock_log):
    # Mock download, unzip, and move folder failure
    # Simulate download and unzip success, but moving folder fails
    mock_download_file_async.return_value = None  # No error
    mock_unzip_file_async.return_value = None  # No error
    mock_moving_file_async.side_effect = Exception("Move folder failed")

    # Call the update function
    result = await update_async()

    # Assertions
    assert result is False, "Update should fail due to moving folder failure"
    mock_log.error.assert_any_call("Update failed : %s", "moving folder failed")
    mock_log.error.assert_any_call("Error : %s", "Move folder failed")
    mock_log.error.assert_any_call("=== Update failed ===")
