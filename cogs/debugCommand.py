# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.
from __future__ import annotations

from typing import Optional

import discord
from discord.ext import commands
from discord.ext.commands import Context
from typing_extensions import Self

from common.config import MODE
from handlers.debugHandler import debugd_handler, debugn_handler, debugs_handler
from utils.cogManager import ProtectedCog
from utils.commandManager import protected_command
from utils.notificationManager import send_notifications
from utils.utils import send_embeds


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
    async def debugd(self: Self, context: Context, last_name: str, first_name: Optional[str] = None) -> None:
        """
        Show debug info for a député by name.

        Parameters:
            last_name (str): The last name of the député.
            first_name (Optional[str]): The optional first name of the député.
        """
        await send_embeds(context, lambda: debugd_handler(last_name, first_name))

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
        await send_embeds(context, lambda: debugs_handler(code_ref))
    @protected_command(
        name="debugn",
        description="Debug command.",
    )
    @debug_command()
    async def debugn(self : Self, context: Context, user: discord.User) -> None:
        """
        TODO
        """
        ref_notifs = await self.bot.database.get_notifications(user.id)
        if len(ref_notifs) == 0:
            embed = discord.Embed(
                description=f"No entry for {user.name} in {context.guild.name}.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)
        else:
            await send_embeds(context, lambda: debugn_handler(ref_notifs))
    @protected_command(
        name="simn",
        description="Debug command.",
    )
    @debug_command()
    async def simn(self : Self, __context: Context) -> None:
        """
        TODO
        """
        await send_notifications(self.bot.database, self.bot.get_user)

async def setup(bot) -> None:
    """
    Setup function to add DebugCommand cog to bot.

    Parameters:
        bot: The Discord bot instance.
    """
    await bot.add_cog(DebugCommand(bot))
