# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
from pathlib import Path
from typing import Tuple
import zipfile
import pytest


@pytest.fixture
def setup_folders(tmp_path: Path) -> Tuple[Path, Path]:
    # Create a temporary source folder and a destination folder
    src_folder: Path = tmp_path / "src_folder"
    dst_folder: Path = tmp_path / "dst_folder"

    # Create some files in the source folder
    os.makedirs(src_folder, exist_ok=True)
    file_in_src: Path = src_folder / "test.txt"

    with open(file_in_src, "w", encoding="utf-8") as f:
        f.write("This is a test file.")

    return src_folder, dst_folder


@pytest.fixture
def valid_zip(tmp_path: Path) -> Tuple[Path, Path]:
    # Create a temporary zip file with a simple test file inside
    zip_file_path: Path = tmp_path / "test.zip"
    file_inside_zip: Path = tmp_path / "test.txt"

    # Write a simple text file inside the zip
    with open(file_inside_zip, "w", encoding="utf-8") as f:
        f.write("This is a test file.")

    # Create the zip file
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        zipf.write(file_inside_zip, os.path.basename(file_inside_zip))

    return zip_file_path, tmp_path
