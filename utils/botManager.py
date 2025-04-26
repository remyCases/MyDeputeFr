# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import asyncio
import os
import platform
import time
from pathlib import Path
from typing import List

import discord
from discord import Intents
from discord.ext import commands
from discord.ext.commands import Context
from typing_extensions import Self

from logger.logger import logger
from config.config import DISCORD_BOT_MODE, DISCORD_CMD_PREFIX, UPDATE_AT_LAUNCH
from download.update import start_planning
from utils.utils import MODE


class DiscordBot(commands.Bot):
    def __init__(self: Self, intents: Intents) -> None:
        """
        This creates custom bot variables so that we can access these variables in cogs more easily.

        For example, The logger is available using the following code:
        - logger # In this class
        - bot.logger # In this file
        - self.bot.logger # In cogs
        """
        super().__init__(
            command_prefix=commands.when_mentioned_or(DISCORD_CMD_PREFIX),
            intents=intents,
            help_command=None,
        )
        self.database = None
        self.bot_prefix: str = DISCORD_CMD_PREFIX
        self.mode: MODE = DISCORD_BOT_MODE

        # to handle blocking messages during updates
        self.update_lock: asyncio.Lock = asyncio.Lock()
        self.is_updating: bool = False

    async def load_cogs(self: Self) -> None:
        """
        The code in this function is executed whenever the bot will start.
        """
        for file in os.listdir(Path("cogs")):
            if file.endswith(".py"):
                extension: str = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                    logger.info(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    logger.error(
                        f"Failed to load extension {extension}\n{exception}"
                    )

    async def setup_hook(self: Self) -> None:
        """
        This will just be executed when the bot starts the first time.
        """
        logger.info(f"Logged in as {self.user.name} in {self.mode} mode")
        logger.info(f"discord.py API version: {discord.__version__}")
        logger.info(f"Python version: {platform.python_version()}")
        logger.info(
            f"Running on: {platform.system()} {platform.release()} ({os.name})"
        )
        logger.info("-------------------")
        await self.load_cogs()

    async def on_ready(self: Self) -> None:
        self.loop.create_task(
            start_planning(bot=self, upload_at_launch=UPDATE_AT_LAUNCH)
        )


    async def on_message(self: Self, message: discord.Message) -> None:
        """
        The code in this event is executed every time someone sends a message, 
        with or without the prefix

        :param message: The message that was sent.
        """

        if message.author == self.user or message.author.bot:
            logger.debug(
                f"Ignored bot message (ID: {message.id}) from {message.author} in #{message.channel}"
            )
            return
        logger.info(
            f"Received message (ID : {message.id}) from {message.author} in #{message.channel}: \"{message.content}\""
        )
        start = time.perf_counter()
        await self.process_commands(message)
        end = time.perf_counter()
        duration = (end - start) * 1000
        logger.debug(
            f"Processed message (ID : {message.id}) from {message.author} in #{message.channel} "
            f"in {duration:.2f} ms"
        )

    async def on_command_completion(self: Self, context: Context) -> None:
        """
        The code in this event is executed every time a normal command has been *successfully* executed.

        :param context: The context of the command that has been executed.
        """
        full_command_name: str = context.command.qualified_name
        split: List[str] = full_command_name.split(" ")
        executed_command: str = str(split[0])
        if context.guild is not None:
            logger.info(
                "Executed %s command in %s (ID: %s) by %s (ID: %s)",
                executed_command, context.guild.name, context.guild.id,
                context.author, context.author.id
            )
        else:
            logger.info(
                "Executed %s command by %s (ID: %s) in DMs",
                executed_command, context.author, context.author.id
            )

    async def on_command_error(self, context: Context, error) -> None:
        """
        The code in this event is executed every time a normal valid command catches an error.

        :param context: The context of the normal command that failed executing.
        :param error: The error that has been faced.
        """
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = discord.Embed(
                description=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                description="You are not the owner of the bot!", color=0xE02B2B
            )
            await context.send(embed=embed)
            if context.guild:
                logger.warning(
                    f"{context.author} (ID: {context.author.id}) tried to execute an owner only command in the guild {context.guild.name} (ID: {context.guild.id}), but the user is not an owner of the bot."
                )
            else:
                logger.warning(
                    "%s (ID: %s) tried to execute an owner only command in the bot's DMs, \
                        but the user is not an owner of the bot.",
                    context.author, context.author.id
                )
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="You are missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to execute this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                description="I am missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to fully perform this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Error!",
                # We need to capitalize because the command arguments have no capital letter in the code
                # and they are the first word in the error message.
                description=str(error).capitalize(),
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        else:
            raise error
