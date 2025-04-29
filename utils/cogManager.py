# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from functools import wraps
from typing import cast

from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.hybrid import T
from typing_extensions import Self

from utils.botManager import DiscordBot


class ProtectedCog(commands.Cog):
    """Class with all commands protected during updates"""
    def __init__(self: Self, bot: DiscordBot) -> None:
        self.bot: DiscordBot = bot
        if not hasattr(bot, "update_lock"):
            raise commands.ExtensionError(
                "Missing lock to handle blocking commands during update.", 
                name="ProtectedCog"
            )

def not_updating():
    """Decorator to ensure commands will not be executed during an update"""
    def decorator(func: T) -> T:
        @wraps(func)
        async def wrapper(cog: ProtectedCog, context: Context, *args, **kwargs):
            if cog.bot.update_lock.locked():
                await context.send(
                    "Le bot est en cours de mise à jour. Service temporairement indisponible."
                )
                return None

            return await func(cog, context, *args, **kwargs)
        return cast(T, wrapper)
    return decorator
