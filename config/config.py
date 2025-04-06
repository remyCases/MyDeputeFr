# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of the MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
import tempfile
from collections.abc import Callable
from types import ModuleType
from logging import Logger
from dotenv import load_dotenv


load_dotenv()

class MissingEnvException(Exception):
    """Exception raised when an environment variable is missing."""

__HIDE_VAL_IN_LOG = ["DISCORD_TOKEN"]  # List of values to hide in the log

def show_config(module: ModuleType, logger: Logger):
    """Displays the attributes of a module, ignoring certain sensitive values."""
    for name, val in module.__dict__.items():
        if not callable(val) and not isinstance(val, ModuleType) and not name.startswith("_"):
            # Hides secret entries in the log
            msg = f"{name} : {val if name not in __HIDE_VAL_IN_LOG else "***secret***"}"
            logger.debug(msg)


def __load_env(name: str, func: Callable[[], str]) -> str:
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

# Updates
# TODO : Set default UPDATE_URL_DOWNLOAD
UPDATE_URL_DOWNLOAD = __load_env("UPDATE_URL_DOWNLOAD", lambda: "")  # URL for downloading updates
UPDATE_HOUR = __load_env("UPDATE_HOUR", lambda: "08:00:00")  # Default update time
UPDATE_AT_LAUNCH = __load_env("UPDATE_AT.LAUNCH", lambda: "TRUE").upper() in ('TRUE', '1', 'T')  # Enable updates at launch
UPDATE_TEMP_FOLDER = __load_env("UPDATE_TEMP_FOLDER", tempfile.mkdtemp)

# Folders
# TODO : As I had to guess the directory structure, confirm that the default path are valid
DATA_FOLDER = __load_env("DATA_FOLDER", lambda: "data")
ACTEUR_FOLDER = __load_env("ACTEUR_FOLDER", lambda: "data/acteur")  # Path to "acteur" folder
ORGANE_FOLDER = __load_env("ORGANE_FOLDER", lambda: "data/organe")  # Path to "organe" folder
SCRUTINS_FOLDER = __load_env("SCRUTINS_FOLDER", lambda: "data/scrutins")  # Path to "scrutins" folder

# Logs
LOG_PATH = __load_env("LOG_PATH", lambda: "discord.log")  # Path to the log file
LOG_LEVEL = __load_env("LOG_LEVEL", lambda: "INFO").upper()  # Logging level (INFO, DEBUG...)
