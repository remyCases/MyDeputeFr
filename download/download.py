# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import asyncio
from concurrent.futures import ThreadPoolExecutor
import aiohttp
import os
import shutil
import tempfile
import zipfile
from datetime import datetime
from logging import Logger
import requests

from config.config import UPDATE_HOUR, UPDATE_URL_DOWNLOAD_SCRUTINS, UPDATE_URL_DOWNLOAD_ACTEUR_ORGANE, SCRUTINS_FOLDER, \
    ACTEUR_FOLDER, ORGANE_FOLDER, UPDATE_PROGRESS_SECOND
from utils.utils import compute_time_for_update

def show_progress(
        p_log: Logger,
        p_url: str,
        p_content_length: int | None,
        p_chunk_size: int,
        p_nb_chunks_wrote: int,
        p_last_show: datetime | None) -> datetime:
    now = datetime.now()
    update_second = UPDATE_PROGRESS_SECOND
    if not p_last_show or (update_second != 0 and (now - p_last_show).seconds > update_second):
        size_wrote_chunks_mb = ((p_chunk_size * p_nb_chunks_wrote) / 1024) / 1024
        ct_length_mb = (int(p_content_length) / 1024) / 1024 if p_content_length else "???"
        p_log.info(f"Download {os.path.basename(p_url)} : {size_wrote_chunks_mb:.2f} MB / {ct_length_mb:.2f} MB")
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
        file_path (str) : The path where the file must write. Path must be writable and the parents folder must exist.
    """
    log.info(f"Downloading {url} to {file_path}")

    content_length = requests.head(url).headers.get("content-length")
    response = requests.get(url, stream=True, timeout=10)
    response.raise_for_status()

    with open(file_path, "wb") as f:
        chunk_size = 8192
        nb_chunks_wrote = 0
        last_show = None
        for chunk in response.iter_content(chunk_size=chunk_size):
            f.write(chunk)
            nb_chunks_wrote += 1
            last_show = show_progress(log, url, content_length, chunk_size, nb_chunks_wrote, last_show)

    log.info(f"Download done")

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
        except aiohttp.ClientConnectionError:
            log.error("Connection error from %s", url)
        except aiohttp.ClientResponseError:
            log.error("Invalid response from %s", url)

    log.info("Download done")


def unzip_file(log: Logger, path: str, dst_folder: str) -> None :
    """
    Unzip a zip file to destination folder.

    Parameters:
        log (Logger) : The logger use by the function.
        path (str): The path of the zip file.
        dst_folder (str) : The path of the destination folder.
    """
    log.info(f"Unzipping file {path} to {dst_folder}")
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
    log.info(f"Moving file from {src_folder} to {dst_folder}")

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

def update_sync(log: Logger) -> bool:
    """
    Update the data folder with fresh data from UPDATE_URL_DOWNLOAD.

    Parameters:
        log (Logger) : The logger use by the function.
    """
    def show_error_on_exception(msg:str, exception: Exception) -> None:
        log.error(f"Update failed : {msg}")
        log.error(f"Error : {str(exception)}")
        log.error("=== Update failed ===")

    log.info("=== Update starting ===")

    with tempfile.TemporaryDirectory() as download_temp, tempfile.TemporaryDirectory() as zip_temp:
        # Download File to zip download folder
        zip_file_scrutins = os.path.join(download_temp, "data_scrutins.zip")
        zip_file_acteur_organe = os.path.join(download_temp, "data_acteur_organe.zip")
        try:
            download_file(log, UPDATE_URL_DOWNLOAD_SCRUTINS, zip_file_scrutins)
            download_file(log, UPDATE_URL_DOWNLOAD_ACTEUR_ORGANE, zip_file_acteur_organe)
        except Exception as e:
            show_error_on_exception("download failed", e)
            return False

        # Unzip File to zip temp folder
        zip_temp_scrutins = os.path.join(zip_temp, "scrutins")
        zip_temp_acteur_organe = os.path.join(zip_temp, "acteur_organe")
        try:
            unzip_file(log, zip_file_scrutins, zip_temp_scrutins)
            unzip_file(log, zip_file_acteur_organe, zip_temp_acteur_organe)
        except Exception as e:
            show_error_on_exception("unzipping failed", e)
            return False

        # Move folder to data folder
        try:
            moving_folder(log, os.path.join(zip_temp_scrutins, "json"), SCRUTINS_FOLDER)
            moving_folder(log, os.path.join(zip_temp_acteur_organe, "json", "acteur"), ACTEUR_FOLDER)
            moving_folder(log, os.path.join(zip_temp_acteur_organe, "json", "organe"), ORGANE_FOLDER)
        except Exception as e:
            show_error_on_exception("moving folder failed", e)
            return False

    log.info("=== Update success ===")
    return True

async def update_async(log: Logger) -> bool:
    """
    Update the data folder with fresh data asynchronously.

    Parameters:
        log (Logger) : The logger use by the function.
    """
    with tempfile.TemporaryDirectory() as download_temp, tempfile.TemporaryDirectory() as zip_temp:
        # Download File to zip download folder
        zip_file_scrutins = os.path.join(download_temp, "data_scrutins.zip")
        zip_file_acteur_organe = os.path.join(download_temp, "data_acteur_organe.zip")
        try:
            await download_file_async(log, UPDATE_URL_DOWNLOAD_SCRUTINS, zip_file_scrutins)
            await download_file_async(log, UPDATE_URL_DOWNLOAD_ACTEUR_ORGANE, zip_file_acteur_organe)
        except Exception as e:
            log.error("download failed %s", e)
            return False

        await asyncio.sleep(0)

        # Unzip File to zip temp folder
        zip_temp_scrutins = os.path.join(zip_temp, "scrutins")
        zip_temp_acteur_organe = os.path.join(zip_temp, "acteur_organe")
        try:
            await unzip_file_async(log, zip_file_scrutins, zip_temp_scrutins)
            await unzip_file_async(log, zip_file_acteur_organe, zip_temp_acteur_organe)
        except Exception as e:
            log.error("unzipping failed %s", e)
            return False

        # Move folder to data folder
        try:
            await moving_folder_async(log,
                                      os.path.join(zip_temp_scrutins, "json"),
                                      SCRUTINS_FOLDER)
            await moving_folder_async(log,
                                      os.path.join(zip_temp_acteur_organe, "json", "acteur"),
                                      ACTEUR_FOLDER)
            await moving_folder_async(log,
                                      os.path.join(zip_temp_acteur_organe, "json", "organe"),
                                      ORGANE_FOLDER)
        except Exception as e:
            log.error("moving folder failed", e)
            return False

    log.info("=== Update success ===")
    return True

async def update(log: Logger, bot):
    """Async version of update ot make it compatible with asyncio"""
    async with bot.update_lock:
        bot.is_updating = True
        try:
            await update_async(log)
        finally:
            bot.is_updating = False

async def start_planning(log: Logger, bot, upload_at_launch: bool) -> None:
    """
    Start update scheduler to update data every UPDATE_HOUR.

    Parameters:
        log (Logger) : The logger use by the function.
        upload_at_launch (bool): If True run an update at launch.
    """
    if upload_at_launch:
        log.info("First update...")
        await update(log, bot)

    while True:
        try:
            target_time, seconds_until_target = compute_time_for_update(UPDATE_HOUR)
        except ValueError as e:
            log.error("Invalid hour format given for updates. Expected '%H:%M:%S' format.")
            raise e

        log.info(f"Update planed at {target_time} in {seconds_until_target} seconds.")
        await asyncio.sleep(seconds_until_target)
        await update(log, bot)
