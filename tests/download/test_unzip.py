# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
import zipfile

import pytest

from download.core import unzip_file_async


@pytest.mark.asyncio
async def test_unzip_file_success(valid_zip, mock_log):
    # Get the zip file path and destination folder
    zip_path, dst_folder = valid_zip

    # Ensure destination folder exists
    os.makedirs(dst_folder, exist_ok=True)

    # Call the unzip function
    await unzip_file_async(mock_log, zip_path, dst_folder)

    # Check logs
    mock_log.info.assert_any_call("Unzipping file %s to %s", zip_path, dst_folder)
    mock_log.info.assert_any_call("Unzip done")

    # Check if the file has been extracted
    extracted_file_path = os.path.join(dst_folder, "test.txt")
    assert os.path.exists(extracted_file_path), "Extracted file not found in destination folder"

    # Check the content of the extracted file
    with open(extracted_file_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == "This is a test file.", "Content of extracted file is incorrect"

@pytest.mark.asyncio
async def test_unzip_file_bad_zip(tmpdir, mock_log):
    # Create an invalid zip file (not actually a zip file)
    bad_zip_path = tmpdir.join("bad.zip")
    with open(bad_zip_path, "w", encoding="utf-8") as f:
        f.write("This is not a zip file.")

    # Call the unzip function and expect it to raise an exception
    with pytest.raises(zipfile.BadZipFile):
        await unzip_file_async(mock_log, str(bad_zip_path), str(tmpdir))

@pytest.mark.asyncio
async def test_unzip_file_file_not_found(tmpdir, mock_log):
    # Simulate a FileNotFoundError by providing a non-existent file path
    non_existent_zip_path = tmpdir.join("non_existent.zip")

    # Call the unzip function and expect it to raise an exception
    with pytest.raises(FileNotFoundError):
        await unzip_file_async(mock_log, str(non_existent_zip_path), str(tmpdir))
