# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from unittest.mock import patch, MagicMock

from config import config
from download.download import update
from tests.common import mock_log


def test_update_success(mock_log):
    # Setup
    mock_temp_dir_path = "/tmp_dir/"
    mock_temp_dir_context_manager = MagicMock()
    mock_temp_dir_context_manager.__enter__.return_value = mock_temp_dir_path
    mock_temp_dir = MagicMock(return_value=mock_temp_dir_context_manager)


    # Mock the functions used in the update process
    with ( patch('download.download.download_file') as mock_download_file, \
            patch('download.download.unzip_file') as mock_unzip_file, \
            patch('download.download.moving_folder') as mock_moving_folder, \
            patch('tempfile.TemporaryDirectory', mock_temp_dir)):
        # Mock the behavior of each function to simulate success
        mock_download_file.return_value = None  # No error
        mock_unzip_file.return_value = None  # No error
        mock_moving_folder.return_value = None  # No error

        # Call the update function
        result = update(mock_log)

        # Assertions
        assert result is True, "Update should succeed"
        mock_log.info.assert_any_call("=== Update starting ===")
        mock_log.info.assert_any_call("=== Update success ===")

        # Check that the functions were called correctly
        mock_download_file.assert_any_call(mock_log, config.UPDATE_URL_DOWNLOAD_SCRUTINS, '/tmp_dir/data_scrutins.zip')
        mock_download_file.assert_any_call(mock_log, config.UPDATE_URL_DOWNLOAD_ACTEUR_ORGANE, '/tmp_dir/data_acteur_organe.zip')
        mock_unzip_file.assert_any_call(mock_log, '/tmp_dir/data_scrutins.zip', '/tmp_dir/scrutins')
        mock_unzip_file.assert_any_call(mock_log, '/tmp_dir/data_acteur_organe.zip', '/tmp_dir/acteur_organe')
        mock_moving_folder.assert_any_call(mock_log, '/tmp_dir/scrutins/json', config.SCRUTINS_FOLDER)
        mock_moving_folder.assert_any_call(mock_log, '/tmp_dir/acteur_organe/json/acteur', config.ACTEUR_FOLDER)
        mock_moving_folder.assert_any_call(mock_log, '/tmp_dir/acteur_organe/json/organe', config.ORGANE_FOLDER)


def test_update_download_fail(mock_log):
    # Mock download failure (download_file raises an exception)
    with patch('download.download.download_file') as mock_download_file:
        mock_download_file.side_effect = Exception("Download failed")

        # Call the update function
        result = update(mock_log)

        # Assertions
        assert result is False, "Update should fail due to download failure"
        mock_log.error.assert_any_call("Update failed : download failed")
        mock_log.error.assert_any_call("Error : Download failed")
        mock_log.error.assert_any_call("=== Update failed ===")


def test_update_unzip_fail(mock_log):
    # Mock download and unzip failure
    with patch('download.download.download_file') as mock_download_file, \
            patch('download.download.unzip_file') as mock_unzip_file:
        # Simulate download success but unzip failure
        mock_download_file.return_value = None  # No error
        mock_unzip_file.side_effect = Exception("Unzip failed")

        # Call the update function
        result = update(mock_log)

        # Assertions
        assert result is False, "Update should fail due to unzip failure"
        mock_log.error.assert_any_call("Update failed : unzipping failed")
        mock_log.error.assert_any_call("Error : Unzip failed")
        mock_log.error.assert_any_call("=== Update failed ===")


def test_update_move_fail(mock_log):
    # Mock download, unzip, and move folder failure
    with patch('download.download.download_file') as mock_download_file, \
            patch('download.download.unzip_file') as mock_unzip_file, \
            patch('download.download.moving_folder') as mock_moving_folder:
        # Simulate download and unzip success, but moving folder fails
        mock_download_file.return_value = None  # No error
        mock_unzip_file.return_value = None  # No error
        mock_moving_folder.side_effect = Exception("Move folder failed")

        # Call the update function
        result = update(mock_log)

        # Assertions
        assert result is False, "Update should fail due to moving folder failure"
        mock_log.error.assert_any_call("Update failed : moving folder failed")
        mock_log.error.assert_any_call("Error : Move folder failed")
        mock_log.error.assert_any_call("=== Update failed ===")
