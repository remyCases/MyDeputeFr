# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from pathlib import Path
from unittest.mock import call, patch, MagicMock

import pytest

from config import config
from download.update import update_async, update_scrutins, update_acteur_organe

@pytest.mark.asyncio
@patch("download.update.moving_folder_async")
@patch("download.update.unzip_file_async")
@patch("download.update.download_file_async")
async def test_update_scrutins_success(
    mock_download_file_async,
    mock_unzip_file_async,
    mock_moving_file_async,
    mock_log):
    # Setup
    mock_temp_dir_path = Path("/tmp_dir/")

    # Mock the behavior of each function to simulate success
    mock_download_file_async.return_value = None  # No error
    mock_unzip_file_async.return_value = None  # No error
    mock_moving_file_async.return_value = None  # No error

    # Call the update function
    result = await update_scrutins(mock_log, mock_temp_dir_path, mock_temp_dir_path)

    # Assertions
    assert result is None, "Update should succeed"
    mock_download_file_async.assert_has_calls([
        call(mock_log, config.UPDATE_URL_DOWNLOAD_SCRUTINS, Path("/tmp_dir/data_scrutins.zip"))
    ])
    mock_unzip_file_async.assert_has_calls([
        call(mock_log, Path("/tmp_dir/data_scrutins.zip"), Path("/tmp_dir/scrutins"))
    ])
    mock_moving_file_async.assert_has_calls([
        call(mock_log, Path("/tmp_dir/scrutins/json"), config.SCRUTINS_FOLDER)
    ])
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()

@pytest.mark.asyncio
@patch("download.update.download_file_async")
async def test_update_scrutins_download_fail(
    mock_download_file_async,
    mock_log):
    # Mock download failure (download_file raises an exception)
    mock_download_file_async.side_effect = Exception("Download failed")

    # Call the update function
    with pytest.raises(Exception):
        await update_scrutins(mock_log, Path(), Path())

    # Assertions
    mock_log.error.assert_has_calls([
        call("Update failed : %s", "download failed"),
        call("Error : %s", "Download failed"),
        call("=== Update failed ===")
    ])
    mock_log.info.assert_not_called()

@pytest.mark.asyncio
@patch("download.update.unzip_file_async")
@patch("download.update.download_file_async")
async def test_update_scrutins_unzip_fail(
    mock_download_file_async,
    mock_unzip_file_async,
    mock_log):
    # Mock download success and unzip failure
    mock_download_file_async.return_value = None  # No error
    mock_unzip_file_async.side_effect = Exception("Unzip failed")

    # Call the update function
    with pytest.raises(Exception):
        await update_scrutins(mock_log, Path(), Path())

    # Assertions
    mock_log.error.assert_has_calls([
        call("Update failed : %s", "unzipping failed"),
        call("Error : %s", "Unzip failed"),
        call("=== Update failed ===")
    ])
    mock_log.info.assert_not_called()

@pytest.mark.asyncio
@patch("download.update.moving_folder_async")
@patch("download.update.unzip_file_async")
@patch("download.update.download_file_async")
async def test_update_scrutins_move_fail(
    mock_download_file_async,
    mock_unzip_file_async,
    mock_moving_file_async, mock_log):
    # Mock download and unzip success, and move folder failure
    mock_download_file_async.return_value = None  # No error
    mock_unzip_file_async.return_value = None  # No error
    mock_moving_file_async.side_effect = Exception("Move folder failed")

    # Call the update function
    with pytest.raises(Exception):
        await update_scrutins(mock_log, Path(), Path())

    # Assertions
    mock_log.error.assert_has_calls([
        call("Update failed : %s", "moving folder failed"),
        call("Error : %s", "Move folder failed"),
        call("=== Update failed ===")
    ])
    mock_log.info.assert_not_called()

@pytest.mark.asyncio
@patch("download.update.moving_folder_async")
@patch("download.update.unzip_file_async")
@patch("download.update.download_file_async")
async def test_update_acteur_organe_success(
    mock_download_file_async,
    mock_unzip_file_async,
    mock_moving_file_async,
    mock_log):
    # Setup
    mock_temp_dir_path = Path("/tmp_dir/")

    # Mock the behavior of each function to simulate success
    mock_download_file_async.return_value = None  # No error
    mock_unzip_file_async.return_value = None  # No error
    mock_moving_file_async.return_value = None  # No error

    # Call the update function
    result = await update_acteur_organe(mock_log, mock_temp_dir_path, mock_temp_dir_path)

    # Assertions
    assert result is None, "Update should succeed"
    mock_download_file_async.assert_has_calls([
        call(mock_log, config.UPDATE_URL_DOWNLOAD_ACTEUR_ORGANE, Path("/tmp_dir/data_acteur_organe.zip"))
    ])
    mock_unzip_file_async.assert_has_calls([
        call(mock_log, Path("/tmp_dir/data_acteur_organe.zip"), Path("/tmp_dir/acteur_organe"))
    ])
    mock_moving_file_async.assert_has_calls([
        call(mock_log, Path("/tmp_dir/acteur_organe/json/acteur"), config.ACTEUR_FOLDER),
        call(mock_log, Path("/tmp_dir/acteur_organe/json/organe"), config.ORGANE_FOLDER),
    ])
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()

@pytest.mark.asyncio
@patch("download.update.download_file_async")
async def test_update_acteur_organe_download_fail(
    mock_download_file_async,
    mock_log):
    # Mock download failure (download_file raises an exception)
    mock_download_file_async.side_effect = Exception("Download failed")

    # Call the update function
    with pytest.raises(Exception):
        await update_acteur_organe(mock_log, Path(), Path())

    # Assertions
    mock_log.error.assert_has_calls([
        call("Update failed : %s", "download failed"),
        call("Error : %s", "Download failed"),
        call("=== Update failed ===")
    ])
    mock_log.info.assert_not_called()

@pytest.mark.asyncio
@patch("download.update.unzip_file_async")
@patch("download.update.download_file_async")
async def test_update_acteur_organe_unzip_fail(
    mock_download_file_async,
    mock_unzip_file_async,
    mock_log):
    # Mock download and unzip failure
    mock_download_file_async.return_value = None  # No error
    mock_unzip_file_async.side_effect = Exception("Unzip failed")

    # Call the update function
    with pytest.raises(Exception):
        await update_acteur_organe(mock_log, Path(), Path())

    # Assertions
    mock_log.error.assert_has_calls([
        call("Update failed : %s", "unzipping failed"),
        call("Error : %s", "Unzip failed"),
        call("=== Update failed ===")
    ])
    mock_log.info.assert_not_called()

@pytest.mark.asyncio
@patch("download.update.moving_folder_async")
@patch("download.update.unzip_file_async")
@patch("download.update.download_file_async")
async def test_update_acteur_organe_move_fail(
    mock_download_file_async,
    mock_unzip_file_async,
    mock_moving_file_async, mock_log):
    # Mock download, unzip, and move folder failure
    # Simulate download and unzip success, but moving folder fails
    mock_download_file_async.return_value = None  # No error
    mock_unzip_file_async.return_value = None  # No error
    mock_moving_file_async.side_effect = Exception("Move folder failed")

    # Call the update function
    with pytest.raises(Exception):
        await update_acteur_organe(mock_log, Path(), Path())

    # Assertions
    mock_log.error.assert_has_calls([
        call("Update failed : %s", "moving folder failed"),
        call("Error : %s", "Move folder failed"),
        call("=== Update failed ===")
    ])
    mock_log.info.assert_not_called()

@pytest.mark.asyncio
@patch("download.update.update_scrutins")
@patch("download.update.update_acteur_organe")
async def test_update_async_success(
    mock_update_scrutins,
    mock_update_acteur_organe,
    mock_log):

    # Mock the behavior of each function to simulate success
    mock_update_scrutins.return_value = None  # No error
    mock_update_acteur_organe.return_value = None  # No error

    # Call the update function
    result = await update_async(mock_log, True)

    # Assertions
    assert result is True, "Update should succeed"
    mock_log.info.assert_has_calls([
        call("=== Update starting ==="),
        call("=== Update success ===")
    ])
    mock_log.error.assert_not_called()

@pytest.mark.asyncio
@patch("download.update.update_scrutins")
async def test_update_async_scrutins_fail(
    mock_update_scrutins,
    mock_log):

    mock_temp_dir_path = Path("/tmp_dir/")
    mock_temp_dir_context_manager = MagicMock()
    mock_temp_dir_context_manager.__enter__.return_value = mock_temp_dir_path
    mock_temp_dir = MagicMock(return_value=mock_temp_dir_context_manager)

    # Mock the functions used in the update process
    with patch('tempfile.TemporaryDirectory', mock_temp_dir):
        mock_update_scrutins.side_effect = Exception("Scrutins failed")

        # Call the update function
        result = await update_async(mock_log, True)

        # Assertions
        assert result is False, "Update should fail due to scrutins failure"
        mock_log.info.assert_has_calls([
            call("=== Update starting ===")
        ])
        mock_log.error.assert_has_calls([
            call("=== Update scrutins failed ===")
        ])

@pytest.mark.asyncio
@patch("download.update.update_scrutins")
@patch("download.update.update_acteur_organe")
async def test_update_async_acteur_organe_fail(
    mock_update_scrutins,
    mock_update_acteur_organe,
    mock_log):

    mock_temp_dir_path = Path("/tmp_dir/")
    mock_temp_dir_context_manager = MagicMock()
    mock_temp_dir_context_manager.__enter__.return_value = mock_temp_dir_path
    mock_temp_dir = MagicMock(return_value=mock_temp_dir_context_manager)

    # Mock the functions used in the update process
    with patch('tempfile.TemporaryDirectory', mock_temp_dir):
        # Mock download and unzip failure
        mock_update_scrutins.return_value = None  # No error
        mock_update_acteur_organe.side_effect = Exception("Acteur_organe failed")

        # Call the update function
        result = await update_async(mock_log, True)

        # Assertions
        assert result is False, "Update should fail due to acteur_organe failure"
        mock_log.info.assert_has_calls([
            call("=== Update starting ===")
        ])
        mock_log.error.assert_has_calls([
            call("=== Update acteur and organe failed ===")
        ])
