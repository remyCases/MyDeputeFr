# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import asyncio
import os
import tempfile
from logging import Logger

from config.config import UPDATE_HOUR, UPDATE_URL_DOWNLOAD_SCRUTINS,    \
    UPDATE_URL_DOWNLOAD_ACTEUR_ORGANE, SCRUTINS_FOLDER, ACTEUR_FOLDER,  \
    ORGANE_FOLDER
from download.core import download_file, download_file_async,       \
    moving_folder, moving_folder_async, unzip_file, unzip_file_async
from utils.utils import compute_time_for_update


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
            moving_folder(log,
                          os.path.join(zip_temp_scrutins, "json"),
                          SCRUTINS_FOLDER)
            moving_folder(log,
                          os.path.join(zip_temp_acteur_organe, "json", "acteur"),
                          ACTEUR_FOLDER)
            moving_folder(log,
                          os.path.join(zip_temp_acteur_organe, "json", "organe"),
                          ORGANE_FOLDER)
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
        print("in context")
        zip_file_scrutins = os.path.join(download_temp, "data_scrutins.zip")
        zip_file_acteur_organe = os.path.join(download_temp, "data_acteur_organe.zip")
        try:
            print("in try")
            await download_file_async(log,
                                      UPDATE_URL_DOWNLOAD_SCRUTINS,
                                      zip_file_scrutins)
            await download_file_async(log,
                                      UPDATE_URL_DOWNLOAD_ACTEUR_ORGANE,
                                      zip_file_acteur_organe)
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
