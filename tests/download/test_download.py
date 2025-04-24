# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import hashlib
import os
import tempfile

import aiohttp
import pytest
import requests

from download.core import download_file_async


@pytest.mark.asyncio
async def test_download(mock_log):
    """Test a valid download"""
    url = "https://proof.ovh.net/files/1Mb.dat"
    with tempfile.TemporaryDirectory() as download_temp:
        file_path = os.path.join(download_temp, "data.dat")
        await download_file_async(mock_log, url, file_path)
        assert os.path.getsize(file_path) == 1048576, "Invalid size"
        with open(file_path, "rb") as f:
            assert hashlib.md5(f.read()).hexdigest() == "d5eefcccdb834958512bed157d01f3a7", \
                "Invalid md5 hash"

        # Check logs
        mock_log.info.assert_any_call("Downloading %s to %s", url, file_path)
        mock_log.info.assert_any_call("Download done")


@pytest.mark.asyncio
async def test_download_invalid_url(mock_log):
    """Test a download using an invalid url"""
    url = "https:////proof.ovh.net/files/1Mb.dat"
    with tempfile.TemporaryDirectory() as download_temp:
        file_path = os.path.join(download_temp, "data.dat")
        with pytest.raises(aiohttp.InvalidURL):
            await download_file_async(mock_log, url, file_path)

            # Check logs
            mock_log.info.assert_any_call("Connection error from %s", url)

@pytest.mark.asyncio
async def test_download_client_connection_error(mock_log):
    """Test a download using a valid url but from an nonexistent domaine"""
    url = "https://proof.ovh.error/files/1Mb.dat"
    with tempfile.TemporaryDirectory() as download_temp:
        file_path = os.path.join(download_temp, "data.dat")
        with pytest.raises(aiohttp.ClientConnectionError):
            await download_file_async(mock_log, url, file_path)

            # Check logs
            mock_log.info.assert_any_call("Connection error from %s", url)

@pytest.mark.asyncio
async def test_download_client_response_error(mock_log):
    """Test a download using a valid url but for an nonexistent page"""
    url = "https://proof.ovh.net/files/invalid"
    with tempfile.TemporaryDirectory() as download_temp:
        file_path = os.path.join(download_temp, "data.dat")
        with pytest.raises(aiohttp.ClientResponseError):
            await download_file_async(mock_log, url, file_path)

            # Check logs
            mock_log.info.assert_any_call("Invalid response from %s", url)

@pytest.mark.asyncio
async def test_download_invalid_path(mock_log):
    """Test to download in a non existent folder"""
    url = "https://proof.ovh.net/files/1Mb.dat"
    file_path = os.path.join("/do/not/exist", "data.dat")
    with pytest.raises(FileNotFoundError) :
        await download_file_async(mock_log, url, file_path)
