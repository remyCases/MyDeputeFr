# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from datetime import datetime, timedelta
from enum import Enum
from logging import Logger
from os import PathLike
from typing import Tuple, Generator

from logger.logger import logger


def compute_time_for_update(update_hour: str) -> Tuple[datetime, float]:
    """Return the seconds for the next update"""
    try:
        update_time: datetime = datetime.strptime(update_hour, "%H:%M:%S")
    except ValueError as e:
        raise e

    now: datetime = datetime.now()
    target_time: datetime = now.replace(
        hour=update_time.hour,
        minute=update_time.minute,
        second=update_time.second,
        microsecond=0
    )
    if now >= target_time:
        target_time = target_time + timedelta(days=1)

    return target_time, (target_time - now).total_seconds()


def read_files_from_directory(directory: PathLike) -> Generator[dict, None, None]:
    """
    Reads and yields the JSON data of each file in a given directory.
    Skips files that cannot be read or parsed.

    Parameters:
        directory PathLike: The directory containing the files to be read.

    Yields:
        dict: The parsed JSON data from each file.
    """
    for file in os.listdir(directory):
        file_path = directory / file
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                yield json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            logger.error("Error reading %s: %s", file, e)
            continue


async def send_embeds(context: Context, handler : Callable):
    """
    Send a list of embeds to the context.

    Parameters:
        context (Context): The context in which to send the embeds.
        handler: A function that returns a list of embeds or an embed.
    """
    embeds_or_embed = handler()
    if isinstance(embeds_or_embed, list):
        for embed in embeds_or_embed:
            await context.send(embed=embed)
    else:
        await context.send(embed=embeds_or_embed)