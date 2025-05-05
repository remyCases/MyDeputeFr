# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from datetime import datetime
from pathlib import Path
from unittest.mock import call, patch, MagicMock

import pytest

from config import config
from download.update import start_planning, update, \
    update_async, update_scrutins, update_acteur_organe


@pytest.mark.asyncio
@patch("download.update.logger")
@patch("download.update.moving_folder_async")
@patch("download.update.unzip_file_async")
@patch("download.update.download_file_async")
async def test_update_scrutins_success(
    mock_download_file_async: MagicMock,
    mock_unzip_file_async: MagicMock,
    mock_moving_file_async: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:
    # Setup
    mock_temp_dir_path = Path("/tmp_dir/")

    # Mock the behavior of each function to simulate success
    mock_download_file_async.return_value = None  # No error
    mock_unzip_file_async.return_value = None  # No error
    mock_moving_file_async.return_value = None  # No error

    # Call the update_scrutins function
    await update_scrutins(mock_temp_dir_path, mock_temp_dir_path)

    # Assertions subfunctions
    mock_download_file_async.assert_has_calls([
        call(config.UPDATE_URL_DOWNLOAD_SCRUTINS, Path("/tmp_dir/data_scrutins.zip"))
    ])
    mock_unzip_file_async.assert_has_calls([
        call(Path("/tmp_dir/data_scrutins.zip"), Path("/tmp_dir/scrutins"))
    ])
    mock_moving_file_async.assert_has_calls([
        call(Path("/tmp_dir/scrutins/json"), config.SCRUTINS_FOLDER)
    ])

    # Assertions log
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.update.logger")
@patch("download.update.moving_folder_async")
@patch("download.update.unzip_file_async")
@patch("download.update.download_file_async")
async def test_update_scrutins_download_fail(
    mock_download_file_async: MagicMock,
    mock_unzip_file_async: MagicMock,
    mock_moving_file_async: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:
    # Setup
    mock_temp_dir_path = Path("/tmp_dir/")

    # Mock download failure (download_file raises an exception)
    mock_download_file_async.side_effect = Exception("Download failed")

    # Call the update_scrutins function and assert exception
    with pytest.raises(Exception):
        await update_scrutins(mock_temp_dir_path, mock_temp_dir_path)

    # Assertions subfunctions
    mock_download_file_async.assert_has_calls([
        call(config.UPDATE_URL_DOWNLOAD_SCRUTINS, Path("/tmp_dir/data_scrutins.zip"))
    ])
    mock_unzip_file_async.assert_not_called()
    mock_moving_file_async.assert_not_called()

    # Assertions log
    mock_log.error.assert_has_calls([
        call("Update failed : %s", "download failed"),
        call("Error : %s", "Download failed"),
        call("=== Update failed ===")
    ])
    mock_log.info.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.update.logger")
@patch("download.update.moving_folder_async")
@patch("download.update.unzip_file_async")
@patch("download.update.download_file_async")
async def test_update_scrutins_unzip_fail(
    mock_download_file_async: MagicMock,
    mock_unzip_file_async: MagicMock,
    mock_moving_file_async: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:
    # Setup
    mock_temp_dir_path = Path("/tmp_dir/")

    # Mock download success and unzip failure
    mock_download_file_async.return_value = None  # No error
    mock_unzip_file_async.side_effect = Exception("Unzip failed")

    # Call the update_scrutins function and assert exception
    with pytest.raises(Exception):
        await update_scrutins(mock_temp_dir_path, mock_temp_dir_path)

    # Assertions subfunctions
    mock_download_file_async.assert_has_calls([
        call(config.UPDATE_URL_DOWNLOAD_SCRUTINS, Path("/tmp_dir/data_scrutins.zip"))
    ])
    mock_unzip_file_async.assert_has_calls([
        call(Path("/tmp_dir/data_scrutins.zip"), Path("/tmp_dir/scrutins"))
    ])
    mock_moving_file_async.assert_not_called()

    # Assertions log
    mock_log.error.assert_has_calls([
        call("Update failed : %s", "unzipping failed"),
        call("Error : %s", "Unzip failed"),
        call("=== Update failed ===")
    ])
    mock_log.info.assert_not_called()
    mock_log.warning.assert_not_called()

    ## Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.update.logger")
@patch("download.update.moving_folder_async")
@patch("download.update.unzip_file_async")
@patch("download.update.download_file_async")
async def test_update_scrutins_move_fail(
    mock_download_file_async: MagicMock,
    mock_unzip_file_async: MagicMock,
    mock_moving_file_async: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:
    # Setup
    mock_temp_dir_path = Path("/tmp_dir/")

    # Mock download and unzip success, and move folder failure
    mock_download_file_async.return_value = None  # No error
    mock_unzip_file_async.return_value = None  # No error
    mock_moving_file_async.side_effect = Exception("Move folder failed")

    # Call the update_scrutins function and assert exception
    with pytest.raises(Exception):
        await update_scrutins(mock_temp_dir_path, mock_temp_dir_path)

    # Assertions subfunctions
    mock_download_file_async.assert_has_calls([
        call(config.UPDATE_URL_DOWNLOAD_SCRUTINS, Path("/tmp_dir/data_scrutins.zip"))
    ])
    mock_unzip_file_async.assert_has_calls([
        call(Path("/tmp_dir/data_scrutins.zip"), Path("/tmp_dir/scrutins"))
    ])
    mock_moving_file_async.assert_has_calls([
        call(Path("/tmp_dir/scrutins/json"), config.SCRUTINS_FOLDER)
    ])

    # Assertions log
    mock_log.error.assert_has_calls([
        call("Update failed : %s", "moving folder failed"),
        call("Error : %s", "Move folder failed"),
        call("=== Update failed ===")
    ])
    mock_log.info.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.update.logger")
@patch("download.update.moving_folder_async")
@patch("download.update.unzip_file_async")
@patch("download.update.download_file_async")
async def test_update_acteur_organe_success(
    mock_download_file_async: MagicMock,
    mock_unzip_file_async: MagicMock,
    mock_moving_file_async: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:

    # Setup
    mock_temp_dir_path = Path("/tmp_dir/")

    # Mock the behavior of each function to simulate success
    mock_download_file_async.return_value = None  # No error
    mock_unzip_file_async.return_value = None  # No error
    mock_moving_file_async.return_value = None  # No error

    # Call the update_acteur_organe function
    await update_acteur_organe(mock_temp_dir_path, mock_temp_dir_path)

    # Assertions subfunctions
    mock_download_file_async.assert_has_calls([
        call(config.UPDATE_URL_DOWNLOAD_ACTEUR_ORGANE, Path("/tmp_dir/data_acteur_organe.zip"))
    ])
    mock_unzip_file_async.assert_has_calls([
        call(Path("/tmp_dir/data_acteur_organe.zip"), Path("/tmp_dir/acteur_organe"))
    ])
    mock_moving_file_async.assert_has_calls([
        call(Path("/tmp_dir/acteur_organe/json/acteur"), config.ACTEUR_FOLDER),
        call(Path("/tmp_dir/acteur_organe/json/organe"), config.ORGANE_FOLDER),
    ])

    # Assertions log
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.update.logger")
@patch("download.update.moving_folder_async")
@patch("download.update.unzip_file_async")
@patch("download.update.download_file_async")
async def test_update_acteur_organe_download_fail(
    mock_download_file_async: MagicMock,
    mock_unzip_file_async: MagicMock,
    mock_moving_file_async: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:

    # Setup
    mock_temp_dir_path = Path("/tmp_dir/")

    # Mock download failure (download_file raises an exception)
    mock_download_file_async.side_effect = Exception("Download failed")

    # Call the update_acteur_organe function and assert exception
    with pytest.raises(Exception):
        await update_acteur_organe(mock_temp_dir_path, mock_temp_dir_path)

    # Assertions subfunctions
    mock_download_file_async.assert_has_calls([
        call(config.UPDATE_URL_DOWNLOAD_ACTEUR_ORGANE, Path("/tmp_dir/data_acteur_organe.zip"))
    ])
    mock_unzip_file_async.assert_not_called()
    mock_moving_file_async.assert_not_called()

    # Assertions log
    mock_log.error.assert_has_calls([
        call("Update failed : %s", "download failed"),
        call("Error : %s", "Download failed"),
        call("=== Update failed ===")
    ])
    mock_log.info.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.update.logger")
@patch("download.update.moving_folder_async")
@patch("download.update.unzip_file_async")
@patch("download.update.download_file_async")
async def test_update_acteur_organe_unzip_fail(
    mock_download_file_async: MagicMock,
    mock_unzip_file_async: MagicMock,
    mock_moving_file_async: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:

    # Setup
    mock_temp_dir_path = Path("/tmp_dir/")

    # Mock download and unzip failure
    mock_download_file_async.return_value = None  # No error
    mock_unzip_file_async.side_effect = Exception("Unzip failed")

    # Call the update_acteur_organe function and assert exception
    with pytest.raises(Exception):
        await update_acteur_organe(mock_temp_dir_path, mock_temp_dir_path)

    # Assertions subfunctions
    mock_download_file_async.assert_has_calls([
        call(config.UPDATE_URL_DOWNLOAD_ACTEUR_ORGANE, Path("/tmp_dir/data_acteur_organe.zip"))
    ])
    mock_unzip_file_async.assert_has_calls([
        call(Path("/tmp_dir/data_acteur_organe.zip"), Path("/tmp_dir/acteur_organe"))
    ])
    mock_moving_file_async.assert_not_called()

    # Assertions log
    mock_log.error.assert_has_calls([
        call("Update failed : %s", "unzipping failed"),
        call("Error : %s", "Unzip failed"),
        call("=== Update failed ===")
    ])
    mock_log.info.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.update.logger")
@patch("download.update.moving_folder_async")
@patch("download.update.unzip_file_async")
@patch("download.update.download_file_async")
async def test_update_acteur_organe_move_fail(
    mock_download_file_async: MagicMock,
    mock_unzip_file_async: MagicMock,
    mock_moving_file_async: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:

    # Setup
    mock_temp_dir_path = Path("/tmp_dir/")

    # Mock download and unzip success, and move folder failure
    mock_download_file_async.return_value = None  # No error
    mock_unzip_file_async.return_value = None  # No error
    mock_moving_file_async.side_effect = Exception("Move folder failed")

    # Call the update_acteur_organe function and assert exception
    with pytest.raises(Exception):
        await update_acteur_organe(mock_temp_dir_path, mock_temp_dir_path)

    # Assertions subfunctions
    mock_download_file_async.assert_has_calls([
        call(config.UPDATE_URL_DOWNLOAD_ACTEUR_ORGANE, Path("/tmp_dir/data_acteur_organe.zip"))
    ])
    mock_unzip_file_async.assert_has_calls([
        call(Path("/tmp_dir/data_acteur_organe.zip"), Path("/tmp_dir/acteur_organe"))
    ])
    mock_moving_file_async.assert_has_calls([
        call(Path("/tmp_dir/acteur_organe/json/acteur"), config.ACTEUR_FOLDER)
    ])

    # Assertions log
    mock_log.error.assert_has_calls([
        call("Update failed : %s", "moving folder failed"),
        call("Error : %s", "Move folder failed"),
        call("=== Update failed ===")
    ])
    mock_log.info.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.update.logger")
@patch("download.update.update_acteur_organe")
@patch("download.update.update_scrutins")
async def test_update_async_success(
    mock_update_scrutins: MagicMock,
    mock_update_acteur_organe: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:

    # Setup
    mock_temp_dir_path = Path("/tmp_dir/")
    mock_temp_dir_context_manager = MagicMock()
    mock_temp_dir_context_manager.__enter__.return_value = mock_temp_dir_path
    mock_temp_dir = MagicMock(return_value=mock_temp_dir_context_manager)

    with patch('tempfile.TemporaryDirectory', mock_temp_dir):
        # Mock the behavior of each function to simulate success
        mock_update_scrutins.return_value = None  # No error
        mock_update_acteur_organe.return_value = None  # No error

        # Call the update_async function
        await update_async(True)

    # Assertions subfunctions
    mock_update_scrutins.assert_has_calls([
        call(mock_temp_dir_path, mock_temp_dir_path)
    ])
    mock_update_acteur_organe.assert_has_calls([
        call(mock_temp_dir_path, mock_temp_dir_path)
    ])

    # Assertions log
    mock_log.info.assert_has_calls([
        call("=== Update starting ==="),
        call("=== Update success ===")
    ])
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.update.logger")
@patch("download.update.update_acteur_organe")
@patch("download.update.update_scrutins")
async def test_update_async_scrutins_fail(
    mock_update_scrutins: MagicMock,
    mock_update_acteur_organe: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:

    mock_temp_dir_path = Path("/tmp_dir/")
    mock_temp_dir_context_manager = MagicMock()
    mock_temp_dir_context_manager.__enter__.return_value = mock_temp_dir_path
    mock_temp_dir = MagicMock(return_value=mock_temp_dir_context_manager)

    with patch('tempfile.TemporaryDirectory', mock_temp_dir):
        # Mock update_scrutins failure
        mock_update_scrutins.side_effect = Exception("Scrutins failed")

       # Call the update_async function and assert exception
        with pytest.raises(Exception):
            await update_async(True)

    # Assertions subfunctions
    mock_update_scrutins.assert_has_calls([
        call(mock_temp_dir_path, mock_temp_dir_path)
    ])
    mock_update_acteur_organe.assert_not_called()

    # Assertions log
    mock_log.info.assert_has_calls([
        call("=== Update starting ===")
    ])
    mock_log.error.assert_has_calls([
        call("=== Update scrutins failed ===")
    ])
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.update.logger")
@patch("download.update.update_acteur_organe")
@patch("download.update.update_scrutins")
async def test_update_async_acteur_organe_fail(
    mock_update_scrutins: MagicMock,
    mock_update_acteur_organe: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:

    mock_temp_dir_path = Path("/tmp_dir/")
    mock_temp_dir_context_manager = MagicMock()
    mock_temp_dir_context_manager.__enter__.return_value = mock_temp_dir_path
    mock_temp_dir = MagicMock(return_value=mock_temp_dir_context_manager)

    with patch('tempfile.TemporaryDirectory', mock_temp_dir):
        # Mock update_scrutins success and update_acteur_organe failure
        mock_update_scrutins.return_value = None  # No error
        mock_update_acteur_organe.side_effect = Exception("Acteur_organe failed")

       # Call the update_async function and assert exception
        with pytest.raises(Exception):
            await update_async(True)

    # Assertions subfunctions
    mock_update_scrutins.assert_has_calls([
        call(mock_temp_dir_path, mock_temp_dir_path)
    ])
    mock_update_acteur_organe.assert_has_calls([
        call(mock_temp_dir_path, mock_temp_dir_path)
    ])

    # Assertions log
    mock_log.info.assert_has_calls([
        call("=== Update starting ===")
    ])
    mock_log.error.assert_has_calls([
        call("=== Update acteur and organe failed ===")
    ])
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.update.logger")
@patch("download.update.update_async")
async def test_update_success(
    mock_update_async: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:

    mock_update_async.return_value = None  # No error

    # Call the update function
    await update(mock_bot, False)

    # Assertions subfunctions
    mock_update_async.assert_has_calls([
        call(False)
    ])

    # Assertions log
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_awaited_once()
    mock_bot.update_lock.__aexit__.assert_awaited_once()


@pytest.mark.asyncio
@patch("download.update.logger")
@patch("download.update.update_async")
async def test_update_fail(
    mock_update_async: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:

    mock_update_async.side_effect = Exception("Update failed")

    # Call the update function
    await update(mock_bot, False)

    # Assertions subfunctions
    mock_update_async.assert_has_calls([
        call(False)
    ])

    # Assertions log
    mock_log.info.assert_not_called()
    mock_log.error.assert_has_calls([
        call("=== Update failed ===")
    ])
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_awaited_once()
    mock_bot.update_lock.__aexit__.assert_awaited_once()


@pytest.mark.asyncio
@patch("download.update.logger")
@patch("download.update.compute_time_for_update")
@patch("download.update.update")
async def test_start_planning(
    mock_update: MagicMock,
    mock_compute_time_for_update: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:

    mock_update.return_value = None # No error
    target_time = datetime(2020, 5, 17)
    seconds_until_target = .01
    max_iterations = 3
    mock_compute_time_for_update.return_value = (target_time, seconds_until_target)

    # Call the start_planning function
    await start_planning(mock_bot, True, max_iterations=max_iterations)

    # Assertions subfunctions
    assert mock_update.call_count == max_iterations + 1
    mock_update.assert_has_calls([
        call(mock_bot)
    ])

    # Assertions log
    mock_log.info.assert_has_calls([
        call("First update..."),
        call("Update planed at %s in %s seconds.", target_time, seconds_until_target),
        call("Update planed at %s in %s seconds.", target_time, seconds_until_target),
        call("Update planed at %s in %s seconds.", target_time, seconds_until_target),
    ])
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.asyncio
@patch("download.update.logger")
@patch("download.update.compute_time_for_update")
@patch("download.update.update")
async def test_start_planning_update_compute_time_fail(
    mock_update: MagicMock,
    mock_compute_time_for_update: MagicMock,
    mock_log: MagicMock,
    mock_bot: MagicMock) -> None:

    mock_update.return_value = None # No error
    max_iterations = 3
    mock_compute_time_for_update.side_effect = ValueError("Computation failed")

    # Call the start_planning function and assert exception
    with pytest.raises(ValueError):
        await start_planning(mock_bot, True, max_iterations=max_iterations)

    # Assertions subfunctions
    assert mock_update.call_count == 1
    mock_update.assert_has_calls([
        call(mock_bot)
    ])

    # Assertions log
    mock_log.info.assert_has_calls([
        call("First update..."),
    ])
    mock_log.error.assert_has_calls([
        call("Invalid hour format given for updates. Expected '%H:%M:%S' format."),
    ])
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()
