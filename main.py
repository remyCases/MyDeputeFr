"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.3.0
"""

import discord

from config.config import DISCORD_TOKEN, LOG_PATH, LOG_LEVEL, show_config
import config.config
from logger.logger import init_logger
from utils.botManager import DiscordBot

logger = init_logger("discord_bot", LOG_PATH, LOG_LEVEL)
show_config(config.config, logger)

intents = discord.Intents.default()
intents.message_content = True
bot = DiscordBot(intents, logger)
bot.run(DISCORD_TOKEN)
