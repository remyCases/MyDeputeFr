# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import logging
from types import ModuleType
from typing import List

import config.config
from config.config import LOG_LEVEL, LOG_PATH, __HIDE_VAL_IN_LOG

class LoggingFormatter(logging.Formatter):
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        fmt = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        fmt = fmt.replace("(black)", self.black + self.bold)
        fmt = fmt.replace("(reset)", self.reset)
        fmt = fmt.replace("(levelcolor)", log_color)
        fmt = fmt.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(fmt, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


def show_config(module: ModuleType, _logger: logging.Logger, hide_list: List[str]):
    """Displays the attributes of a module, ignoring certain sensitive values."""
    for name, val in module.__dict__.items():
        if not callable(val) and not isinstance(val, ModuleType) and not name.startswith("_"):
            # Hides secret entries in the log
            _logger.debug(
                "%s : %s",
                name, val if name not in hide_list else '***secret***'
            )


def init_logger(log_name: str, file_name: str, log_level: str) -> logging.Logger:
    _logger = logging.getLogger(log_name)
    _logger.setLevel(log_level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(LoggingFormatter())
    # File handler
    file_handler = logging.FileHandler(filename=file_name, encoding="utf-8", mode="w")
    file_handler_formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
    )
    file_handler.setFormatter(file_handler_formatter)

    # Add the handlers
    _logger.addHandler(console_handler)
    _logger.addHandler(file_handler)

    return _logger

logger: logging.Logger = init_logger("discord_bot", LOG_PATH, LOG_LEVEL)
show_config(config.config, logger, __HIDE_VAL_IN_LOG)
