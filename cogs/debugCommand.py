# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from typing_extensions import Self

from discord.ext import commands
from discord.ext.commands import Context

from handlers.debugHandler import debugd_handler, debugs_handler
from utils.cogManager import ProtectedCog
from utils.commandManager import protected_command
from utils.utils import MODE


def debug_command():
    """
    Decorator to allow command only in DEBUG mode.

    Returns:
        Callable: The command decorator to apply.
    """

    async def predicate(ctx: Context):
        if ctx.bot.mode != MODE.DEBUG:
            await ctx.send("Commande non disponible en mode release.")
            return False
        return True

    return commands.check(predicate)


class DebugCommand(ProtectedCog, name="debug"):
    """
    Cog that manages commands related to debug.
    """

    @protected_command(
        name="debugd",
        description="Debug command.",
    )
    @debug_command()
    async def debugd(self: Self, context: Context, name: str) -> None:
        """
        Show debug info for a député by name.

        Parameters:
            context (Context): The context of the command.
            name (str): The name of the député to search.
        """
        await context.send(embed=debugd_handler(name))

    @protected_command(
        name="debugs",
        description="Debug command.",
    )
    @debug_command()
    async def debugs(self : Self, context: Context, code_ref: str) -> None:
        """
        Show debug info for a scrutin by code reference.

        Parameters:
            context (Context): The context of the command.
            code_ref (str): The reference code of the scrutin.
        """
        await context.send(embed=debugs_handler(code_ref))

async def setup(bot) -> None:
    """
    Setup function to add DebugCommand cog to bot.

    Parameters:
        bot: The Discord bot instance.
    """
    await bot.add_cog(DebugCommand(bot))
