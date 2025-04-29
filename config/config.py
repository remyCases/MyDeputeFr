# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from datetime import datetime
import os
from collections.abc import Callable
from logging import Logger
from pathlib import Path
from types import ModuleType

from dotenv import load_dotenv

from utils.utils import MODE

load_dotenv()

class MissingEnvException(Exception):
    """Exception raised when an environment variable is missing."""

__HIDE_VAL_IN_LOG = ["DISCORD_TOKEN"]  # List of values to hide in the log

def show_config(module: ModuleType, logger: Logger):
    """Displays the attributes of a module, ignoring certain sensitive values."""
    for name, val in module.__dict__.items():
        if not callable(val) and not isinstance(val, ModuleType) and not name.startswith("_"):
            # Hides secret entries in the log
            msg = f"{name} : {val if name not in __HIDE_VAL_IN_LOG else '***secret***'}"
            logger.debug(msg)


def __load_env(name: str, func: Callable) -> str:
    """Loads an environment variable either from the environment or from a default generating function."""
    value = os.getenv(name)
    return value if value else func()


def __load_env_required(name: str) -> str:
    """Loads a required environment variable."""
    token = os.getenv(name)
    if not token:
        raise MissingEnvException(f"The environment variable {name} is required")
    return token


# Discord Bot
DISCORD_TOKEN = __load_env_required("DISCORD_TOKEN")  # Discord bot token
DISCORD_CMD_PREFIX = __load_env("DISCORD_CMD_PREFIX", lambda: "!")  # Bot command prefix
DISCORD_BOT_MODE = MODE[__load_env("DISCORD_BOT_MODE", lambda: "RELEASE").upper()]
DISCORD_EMBED_COLOR_MSG =  int(__load_env("DISCORD_EMBED_COLOR", lambda: "0x367588"), 16)
DISCORD_EMBED_COLOR_ERR =  int(__load_env("DISCORD_EMBED_COLOR_ERR", lambda: "0xE02B2B"), 16)
DISCORD_EMBED_COLOR_DEBUG =  int(__load_env("DISCORD_EMBED_COLOR_DEBUG", lambda: "0xFFFFFF"), 16)

# Updates
UPDATE_URL_DOWNLOAD_SCRUTINS = __load_env(
    "UPDATE_URL_DOWNLOAD_SCRUTINS",
    lambda: "https://data.assemblee-nationale.fr/static/openData/repository/17/loi/scrutins/Scrutins.json.zip"
) # URL to update Scrutins
UPDATE_URL_DOWNLOAD_ACTEUR_ORGANE = __load_env(
    "UPDATE_URL_DOWNLOAD_ACTEUR_ORGANE", lambda:
    "https://data.assemblee-nationale.fr/static/openData/repository/17/amo/deputes_actifs_mandats_actifs_organes/"
    "AMO10_deputes_actifs_mandats_actifs_organes.json.zip") # URL to update acteur et organe
UPDATE_HOUR = __load_env("UPDATE_HOUR", lambda: "08:00:00")  # Default update time
UPDATE_AT_LAUNCH = __load_env("UPDATE_AT_LAUNCH", lambda: "TRUE").upper() in ("TRUE", "1", "T")  # Enable updates at launch
UPDATE_PROGRESS_SECOND = int(__load_env("UPDATE_DOWNLOAD_PROGRESS_SECOND", lambda: "2")) # Download progress update in second, if 0 is disabled

NOTIF_HOUR = __load_env("NOTIF_HOUR", lambda: "12:00:00")  # Default update time
MIN_DATE_CURRENT_MOTION = datetime(2023, 1, 1).date()

# Folders to save json data
ACTEUR_FOLDER = Path(__load_env("ACTEUR_FOLDER", lambda: "data/acteur"))
ORGANE_FOLDER = Path(__load_env("ORGANE_FOLDER", lambda: "data/organe"))
SCRUTINS_FOLDER = Path(__load_env("SCRUTINS_FOLDER", lambda: "data/scrutins"))
# Folder for persistent data
DATABASE_FOLDER = Path(__load_env("DATABASE_FOLDER", lambda: "database"))

# Logs
LOG_PATH = __load_env("LOG_PATH", lambda: "discord.log")  # Path to the log file
LOG_LEVEL = __load_env("LOG_LEVEL", lambda: "INFO").upper()  # Logging level (INFO, DEBUG...)
