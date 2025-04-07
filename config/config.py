# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
from collections.abc import Callable
from logging import Logger
from types import ModuleType

from dotenv import load_dotenv

load_dotenv()

class MissingEnvException(Exception):
    """Exception raised when an environment variable is missing."""

__HIDE_VAL_IN_LOG = ["DISCORD_TOKEN", "TCP_TOKEN"]  # List of values to hide in the log

def show_config(module: ModuleType, logger: Logger):
    """Displays the attributes of a module, ignoring certain sensitive values."""
    for name, val in module.__dict__.items():
        if not callable(val) and not isinstance(val, ModuleType) and not name.startswith("_"):
            # Hides secret entries in the log
            msg = f"{name} : {val if name not in __HIDE_VAL_IN_LOG else '***secret***'}"
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
UPDATE_URL_DOWNLOAD_SCRUTINS = __load_env(
    "UPDATE_URL_DOWNLOAD_SCRUTINS",
    lambda: "https://data.assemblee-nationale.fr/static/openData/repository/17/loi/scrutins/Scrutins.json.zip"
) # URL to update Scrutins
UPDATE_URL_DOWNLOAD_ACTEUR_ORGANE = __load_env(
    "UPDATE_URL_DOWNLOAD_ACTEUR_ORGANE", lambda:
    "https://data.assemblee-nationale.fr/static/openData/repository/17/amo/deputes_actifs_mandats_actifs_organes/"
    "AMO10_deputes_actifs_mandats_actifs_organes.json.zip") # URL to update acteur et organe
UPDATE_HOUR = __load_env("UPDATE_HOUR", lambda: "08:00:00")  # Default update time
UPDATE_AT_LAUNCH = __load_env("UPDATE_AT_LAUNCH", lambda: "TRUE").upper() in ('TRUE', '1', 'T')  # Enable updates at launch
UPDATE_PROGRESS_SECOND = int(__load_env("UPDATE_DOWNLOAD_PROGRESS_SECOND", lambda: "2")) # Download progress update in second, if 0 is disabled

# Folders
ACTEUR_FOLDER = __load_env("ACTEUR_FOLDER", lambda: "data/acteur")  # Path to "acteur" folder
ORGANE_FOLDER = __load_env("ORGANE_FOLDER", lambda: "data/organe")  # Path to "organe" folder
SCRUTINS_FOLDER = __load_env("SCRUTINS_FOLDER", lambda: "data/scrutins")  # Path to "scrutins" folder

# Logs
LOG_PATH = __load_env("LOG_PATH", lambda: "discord.log")  # Path to the log file
LOG_LEVEL = __load_env("LOG_LEVEL", lambda: "INFO").upper()  # Logging level (INFO, DEBUG...)

# TCP connection
TCP_TOKEN = __load_env_required("TCP_TOKEN")
TCP_SERVER_HOST = __load_env("TCP_SERVER_HOST", lambda: "127.0.0.1")
TCP_SERVER_PORT = __load_env("TCP_SERVER_PORT", lambda: "8733")
