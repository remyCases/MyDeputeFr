# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from functools import wraps
from typing import Any, Callable, Self, TypeVar, cast
import inspect
from discord.ext import commands

# Generic type for typing commands
T = TypeVar('T', bound=Callable[..., Any])

def not_updating() -> Callable[[T], T]:
    """Decorator to ensure commands will not be executed during an update"""
    def decorator(func: T) -> T:
        @wraps(func)
        async def wrapper(cog, context, *args, **kwargs):
            if cog.bot.update_lock.locked() or cog.bot.is_updating:
                await context.send(
                    "Le bot est en cours de mise à jour. Service temporairement indisponible."
                )
                return None

            # using lock for security
            async with cog.bot.update_lock:
                return await func(cog, context, *args, **kwargs)

        return cast(T, wrapper)
    return decorator

def allow_during_update(func):
    """Decorator to bypass the protection during updates"""
    func.allow_during_update = True
    return func

class ProtectedDuringUpdateCog(commands.Cog):
    """Class with all commands protected during updates"""
    def __init__(self: Self, bot) -> None:
        self.bot = bot
        if not hasattr(bot, "update_lock"):
            raise commands.ExtensionError(
                "Missing lock to handle blocking commands during update.", 
                name="ProtectedDuringUpdateCog"
            )

        # Apply not_updating decorator to all methods that are a command
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if isinstance(method, commands.Command) or hasattr(method, "__command_flag__"):
                if not getattr(method, "allow_during_update", False):
                    setattr(self, name, not_updating()(method))
