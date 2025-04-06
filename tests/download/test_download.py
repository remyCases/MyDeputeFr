# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import hashlib
import os
import tempfile

import pytest
import requests

from download.download import download_file
from tests.common import mock_log


def test_download(mock_log):
    url = "https://proof.ovh.net/files/1Mb.dat"
    with tempfile.TemporaryDirectory() as download_temp:
        file_path = os.path.join(download_temp, "data.dat")
        download_file(mock_log, url, file_path)
        assert os.path.getsize(file_path) == 1048576, "Invalid size"
        with open(file_path,'rb') as f:
            assert hashlib.md5(f.read()).hexdigest() == "d5eefcccdb834958512bed157d01f3a7", "Invalid md5 hash"

        # Check logs
        mock_log.info.assert_any_call(f"Downloading {url} to {file_path}")
        mock_log.info.assert_any_call("Download done")


def test_download_invalid_url(mock_log):
    url = "https://proof.ovh.error/files/1Mb.dat"
    with tempfile.TemporaryDirectory() as download_temp:
        file_path = os.path.join(download_temp, "data.dat")
        with pytest.raises(requests.exceptions.ConnectionError):
            download_file(mock_log, url, file_path)

def test_download_invalid_path(mock_log):
    url = "https://proof.ovh.net/files/1Mb.dat"
    file_path = os.path.join("/do/not/exist", "data.dat")
    with pytest.raises(FileNotFoundError) :
        download_file(mock_log, url, file_path)