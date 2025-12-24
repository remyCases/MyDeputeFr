# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from __future__ import annotations

from functools import wraps
from typing import Callable, Optional, cast

import discord
from discord.ext import commands
from discord.ext.commands._types import Coro
from typing_extensions import Self, Concatenate

from common.config import DISCORD_EMBED_COLOR_STATUS
from utils.botManager import DiscordBot
from utils.types import P, T, ContextT


class ProtectedCog(commands.Cog):
    """Class with all commands protected during updates"""
    def __init__(self: Self, bot: DiscordBot) -> None:
        self.bot: DiscordBot = bot
        if not hasattr(bot, "update_lock"):
            raise commands.ExtensionError(
                "Missing lock to handle blocking commands during update.", 
                name="ProtectedCog"
            )

PCommandCallback = Callable[Concatenate[ProtectedCog, ContextT, P], Coro[Optional[T]]]

def not_updating() -> Callable[[PCommandCallback[ContextT, P, T]], PCommandCallback[ContextT, P, T]]:
    """Decorator to ensure commands will not be executed during an update"""
    def decorator(func: PCommandCallback[ContextT, P, T]) -> PCommandCallback[ContextT, P, T]:
        @wraps(func)
        async def wrapper(cog: ProtectedCog, context: ContextT, *args, **kwargs) -> Optional[T]:
            if cog.bot.update_lock.locked():
                await context.send(embed=discord.Embed(
                    description="Le bot est en cours de mise à jour. Service temporairement indisponible.",
                    color=DISCORD_EMBED_COLOR_STATUS
                ))
                return None

            return await func(cog, context, *args, **kwargs)
        return cast(PCommandCallback[ContextT, P, T], wrapper)
    return decorator
