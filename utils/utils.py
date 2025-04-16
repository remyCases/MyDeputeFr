# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from datetime import datetime, timedelta
from enum import Enum
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
