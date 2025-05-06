"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.3.0
"""

import discord

from common.config import DISCORD_TOKEN
from utils.botManager import DiscordBot

intents = discord.Intents.default()
intents.message_content = True
bot = DiscordBot(intents)
bot.run(DISCORD_TOKEN)
