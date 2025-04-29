# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import discord
from discord.ext import commands
from utils.cogManager import ProtectedCog

class GeneralCommands(ProtectedCog):
    @commands.hybrid_command(
        name="status",
        description="Affiche le statut du bot."
    )
    async def status(self, context) -> None:
        """Basic command to check if the bot is updating or available"""

        if self.bot.update_lock.locked():
            embed = discord.Embed(
                title=":red_circle: Indisponible",
                description="Le bot est en cours de mise à jour.",
                color=0x367588,
            )
        else:
            embed = discord.Embed(
                title=":green_circle: Disponible",
                description="Le bot est disponible.",
                color=0x367588,
            )

        await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(GeneralCommands(bot))
