# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
import zipfile
import pytest

pytest_plugins = ['pytest_asyncio']

@pytest.fixture
def setup_folders(tmpdir):
    # Create a temporary source folder and a destination folder
    src_folder = tmpdir.join("src_folder")
    dst_folder = tmpdir.join("dst_folder")

    # Create some files in the source folder
    os.makedirs(src_folder, exist_ok=True)
    file_in_src = src_folder.join("test.txt")
    with open(file_in_src, "w", encoding="utf-8") as f:
        f.write("This is a test file.")

    return str(src_folder), str(dst_folder)

@pytest.fixture
def valid_zip(tmpdir):
    # Create a temporary zip file with a simple test file inside
    zip_file_path = tmpdir.join("test.zip")
    file_inside_zip = tmpdir.join("test.txt")

    # Write a simple text file inside the zip
    with open(file_inside_zip, "w", encoding="utf-8") as f:
        f.write("This is a test file.")

    # Create the zip file
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        zipf.write(file_inside_zip, os.path.basename(file_inside_zip))

    return str(zip_file_path), str(tmpdir)
