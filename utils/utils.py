# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import json
import os
from datetime import datetime, timedelta
from enum import Enum
from logging import Logger
from os import PathLike
from typing import Tuple


class MODE(Enum):
    """Define the mode of the bot"""
    DEBUG = 0
    RELEASE = 1

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




import os
import json
from typing import Generator, Union
from os import PathLike

def read_files_from_directory(directory: Union[str, PathLike]) -> Generator[dict, None, None]:
    """
    Reads and yields the JSON data of each file in a given directory.
    Skips files that cannot be read or parsed.

    Parameters:
        directory (str | PathLike): The directory containing the files to be read.

    Yields:
        dict: The parsed JSON data from each file.
    """
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                yield json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"Error reading {file}: {e}") # TODO fix to print to log and stdout
            continue
