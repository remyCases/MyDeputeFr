# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
import shutil
import zipfile
from datetime import datetime
from logging import Logger
import aiohttp
import requests

from config.config import UPDATE_PROGRESS_SECOND

def show_progress(
        p_log: Logger,
        p_url: str,
        p_content_length: int | None,
        p_chunk_size: int,
        p_nb_chunks_wrote: int,
        p_last_show: datetime | None) -> datetime:
    """Show progress of download in log"""
    now = datetime.now()
    update_second = UPDATE_PROGRESS_SECOND
    if not p_last_show or (update_second != 0 and (now - p_last_show).seconds > update_second):
        size_wrote_chunks_mb = ((p_chunk_size * p_nb_chunks_wrote) / 1024) / 1024
        ct_length_mb = (int(p_content_length) / 1024) / 1024 if p_content_length else "???"
        p_log.info("Download %s : %f.2f MB / %f.2f MB",
                   os.path.basename(p_url),
                   size_wrote_chunks_mb,
                   ct_length_mb)
        return now
    return p_last_show

def download_file(log: Logger, url: str, file_path: str) -> None :
    """
    Download a file from url to file path.
    Progress will show every DOWNLOAD_UPDATE_SECOND seconds (default 2).
    To hide progress set DOWNLOAD_UPDATE_SECOND to 0.

    Parameters:
        log (Logger) : The logger use by the function.
        url (str) : The url of file to download.
        file_path (str) : 
            The path where the file must write. 
            Path must be writable and the parents folder must exist.
    """
    log.info(f"Downloading {url} to {file_path}")

    content_length = requests.head(url, timeout=10).headers.get("content-length")
    response = requests.get(url, stream=True, timeout=10)
    response.raise_for_status()

    with open(file_path, "wb") as f:
        chunk_size = 8192
        nb_chunks_wrote = 0
        last_show = None
        for chunk in response.iter_content(chunk_size=chunk_size):
            f.write(chunk)
            nb_chunks_wrote += 1
            last_show = show_progress(log, url, content_length, chunk_size,
                                      nb_chunks_wrote, last_show)

    log.info("Download done")

async def download_file_async(log: Logger, url: str, file_path: str) -> None:
    """
    Download a file from url to file path asynchronously.
    Progress will show every DOWNLOAD_UPDATE_SECOND seconds (default 2).
    To hide progress set DOWNLOAD_UPDATE_SECOND to 0.

    Parameters:
        log (Logger) : The logger use by the function.
        url (str) : The url of file to download.
        file_path (str) : 
            The path where the file must write. 
            Path must be writable and the parents folder must exist.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                log.info("Downloading %s to %s", url, file_path)
                content_length = response.headers.get("content-length", 0)
                chunk_size: int = 4096
                nb_chunks_wrote: int = 0
                last_show: datetime | None = None
                with open(file_path, "wb") as f:
                    while True:
                        chunk = await response.content.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        nb_chunks_wrote += 1
                        last_show = show_progress(log, url, content_length,
                                                  chunk_size, nb_chunks_wrote, last_show)
        except (aiohttp.ClientConnectionError, aiohttp.InvalidURL):
            log.error("Connection error from %s", url)
            raise
        except aiohttp.ClientResponseError:
            log.error("Invalid response from %s", url)
            raise

    log.info("Download done")


def unzip_file(log: Logger, path: str, dst_folder: str) -> None :
    """
    Unzip a zip file to destination folder.

    Parameters:
        log (Logger) : The logger use by the function.
        path (str): The path of the zip file.
        dst_folder (str) : The path of the destination folder.
    """
    log.info("Unzipping file %s to %s", path, dst_folder)
    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall(dst_folder)
    log.info("Unzip done")

async def unzip_file_async(log: Logger, path: str, dst_folder: str) -> None:
    """
    Unzip a zip file to destination folder asynchronously.

    Parameters:
        log (Logger) : The logger use by the function.
        path (str): The path of the zip file.
        dst_folder (str) : The path of the destination folder.
    """
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(
            pool,
            lambda: unzip_file(log, path, dst_folder)
        )

def moving_folder(log: Logger, src_folder: str, dst_folder: str) -> None:
    """
    Move the content source folder to destination folder.

    Parameters:
        log (Logger) : The logger use by the function.
        src_folder (str) : The path of source folder to be moved.
        dst_folder (str) : The path of destination folder where the folder must be moved
    """
    log.info("Moving file from %s to %s", src_folder, dst_folder)

    shutil.rmtree(dst_folder, ignore_errors=True)
    shutil.move(src_folder, dst_folder)

    log.info("Move file done")

async def moving_folder_async(log: Logger, src_folder: str, dst_folder: str) -> None:
    """
    Move the content source folder to destination folder asynchronously.

    Parameters:
        log (Logger) : The logger use by the function.
        src_folder (str) : The path of source folder to be moved.
        dst_folder (str) : The path of destination folder where the folder must be moved
    """
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(
            pool,
            lambda: moving_folder(log, src_folder, dst_folder)
        )
