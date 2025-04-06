# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os

import pytest

from download.download import moving_folder
from tests.common import mock_log


@pytest.fixture
def setup_folders(tmpdir):
    # Create a temporary source folder and a destination folder
    src_folder = tmpdir.join("src_folder")
    dst_folder = tmpdir.join("dst_folder")

    # Create some files in the source folder
    os.makedirs(src_folder, exist_ok=True)
    file_in_src = src_folder.join("test.txt")
    with open(file_in_src, 'w') as f:
        f.write("This is a test file.")

    return str(src_folder), str(dst_folder)


def test_moving_folder_success(setup_folders, mock_log):
    # Get the source and destination folders
    src_folder, dst_folder = setup_folders

    # Call the moving_folder function
    moving_folder(mock_log, src_folder, dst_folder)

    # Check logs
    mock_log.info.assert_any_call(f"Moving file from {src_folder} to {dst_folder}")
    mock_log.info.assert_any_call("Move file done")

    # Check if the folder has been moved
    assert os.path.exists(dst_folder), "Source folder was not moved to the destination folder"

    # Check if the file is in the destination folder
    moved_file_path = os.path.join(dst_folder, "test.txt")
    assert os.path.exists(moved_file_path), "File was not moved to the destination folder"

    # Check the content of the moved file
    with open(moved_file_path, 'r') as f:
        content = f.read()
    assert content == "This is a test file.", "Content of the moved file is incorrect"


def test_moving_folder_src_not_exist(mock_log, tmpdir):
    # Set up paths where the source folder doesn't exist
    src_folder = tmpdir.join("non_existent_folder")
    dst_folder = tmpdir.join("dst_folder")

    # Ensure destination folder exists
    os.makedirs(dst_folder, exist_ok=True)

    # Call the moving_folder function and expect a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        moving_folder(mock_log, str(src_folder), str(dst_folder))

