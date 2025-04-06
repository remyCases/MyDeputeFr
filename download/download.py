# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
import shutil
import tempfile
import time
import zipfile
from datetime import datetime
from logging import Logger

import requests
import schedule

from config.config import UPDATE_URL_DOWNLOAD_SCRUTINS, UPDATE_URL_DOWNLOAD_ACTEUR_ORGANE, UPDATE_HOUR, SCRUTINS_FOLDER, \
    ACTEUR_FOLDER, ORGANE_FOLDER, UPDATE_PROGRESS_SECOND


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
    def show_progress(
            p_log: Logger,
            p_url: str,
            p_content_length: int | None,
            p_chunk_size: int,
            p_nb_chunks_wrote: int,
            p_last_show: datetime | None) -> datetime:
        now = datetime.now()
        update_second = UPDATE_PROGRESS_SECOND
        if not last_show or (update_second != 0 and (now - p_last_show).seconds > update_second):
            size_wrote_chunks_mb = ((p_chunk_size * p_nb_chunks_wrote) / 1024) / 1024
            ct_length_mb = (int(p_content_length) / 1024) / 1024 if p_content_length else "???"
            p_log.info(f"Download {os.path.basename(p_url)} : {size_wrote_chunks_mb:.2f} MB / {ct_length_mb:.2f} MB")
            return now
        return p_last_show

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

def update(log: Logger) -> bool:
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

def start_planning(log: Logger, upload_at_launch: bool) -> None:
    """
    Start update scheduler to update data every UPDATE_HOUR.

    Parameters:
        log (Logger) : The logger use by the function.
        upload_at_launch (bool): If True run an update at launch.
    """
    schedule.every().day.at(UPDATE_HOUR).do(update)
    log.info(f"Update planed at {UPDATE_HOUR}")

    if upload_at_launch:
        log.info("First update...")
        update(log)

    while True:
        schedule.run_pending()
        time.sleep(900)  # Check every 15min
