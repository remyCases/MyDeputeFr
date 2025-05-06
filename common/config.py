# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from datetime import datetime
from enum import Enum
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

class MODE(Enum):
    """Define the mode of the bot"""
    DEBUG = 0
    RELEASE = 1


class MissingEnvException(Exception):
    """Exception raised when an environment variable is missing."""


def __load_env(name: str, default: str) -> str:
    """Loads an environment variable either from the environment or from a default generating function."""
    value = os.getenv(name)
    return value if value else default


def __load_env_required(name: str) -> str:
    """Loads a required environment variable."""
    token = os.getenv(name)
    if not token:
        raise MissingEnvException(f"The environment variable {name} is required")
    return token


__HIDE_VAL_IN_LOG = ["DISCORD_TOKEN"]  # List of values to hide in the log
# Discord Bot
DISCORD_TOKEN = __load_env_required("DISCORD_TOKEN")  # Discord bot token
DISCORD_CMD_PREFIX = __load_env("DISCORD_CMD_PREFIX", "!")  # Bot command prefix
DISCORD_BOT_MODE = MODE[__load_env("DISCORD_BOT_MODE", "RELEASE").upper()]
DISCORD_EMBED_COLOR_MSG =  int(__load_env("DISCORD_EMBED_COLOR", "0x367588"), 16)
DISCORD_EMBED_COLOR_ERR =  int(__load_env("DISCORD_EMBED_COLOR_ERR", "0xE02B2B"), 16)
DISCORD_EMBED_COLOR_DEBUG =  int(__load_env("DISCORD_EMBED_COLOR_DEBUG", "0xFFFFFF"), 16)

# Updates
UPDATE_URL_DOWNLOAD_SCRUTINS = __load_env(
    "UPDATE_URL_DOWNLOAD_SCRUTINS",
    "https://data.assemblee-nationale.fr/static/openData/repository/17/loi/scrutins/Scrutins.json.zip"
) # URL to update Scrutins
UPDATE_URL_DOWNLOAD_ACTEUR_ORGANE = __load_env(
    "UPDATE_URL_DOWNLOAD_ACTEUR_ORGANE",
    "https://data.assemblee-nationale.fr/static/openData/repository/17/amo/deputes_actifs_mandats_actifs_organes/"
    "AMO10_deputes_actifs_mandats_actifs_organes.json.zip") # URL to update acteur et organe
UPDATE_HOUR = __load_env("UPDATE_HOUR", "08:00:00")  # Default update time
UPDATE_AT_LAUNCH = __load_env("UPDATE_AT_LAUNCH", "TRUE").upper() in ("TRUE", "1", "T")  # Enable updates at launch
UPDATE_PROGRESS_SECOND = int(__load_env("UPDATE_DOWNLOAD_PROGRESS_SECOND", "2")) # Download progress update in second, if 0 is disabled

NOTIF_HOUR = __load_env("NOTIF_HOUR", "12:00:00")  # Default update time
MIN_DATE_CURRENT_MOTION = datetime(2023, 1, 1).date()

# Folders
ACTEUR_FOLDER = Path(__load_env("ACTEUR_FOLDER", "data/acteur"))  # Path to "acteur" folder
ORGANE_FOLDER = Path(__load_env("ORGANE_FOLDER", "data/organe"))  # Path to "organe" folder
SCRUTINS_FOLDER = Path(__load_env("SCRUTINS_FOLDER", "data/scrutins"))  # Path to "scrutins" folder
# Folder for persistent data
DATABASE_FOLDER = Path(__load_env("DATABASE_FOLDER", "database"))

# Logs
LOG_PATH = __load_env("LOG_PATH", "discord.log")  # Path to the log file
LOG_LEVEL = __load_env("LOG_LEVEL", "INFO").upper()  # Logging level (INFO, DEBUG...)
