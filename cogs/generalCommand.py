# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from discord.ext import commands
from utils.cogManager import ProtectedDuringUpdateCog, allow_during_update

class GeneralCommands(ProtectedDuringUpdateCog):
    @commands.hybrid_command(
        name="status",
        description="Affiche le statut du bot."
    )
    @allow_during_update
    async def status(self, context) -> None:
        """Basic command to check if the bot is updating or available"""
        status = "en cours de mise à jour" if self.bot.is_updating else "disponible"
        await context.send(f"Le bot est en ligne et {status}!")

async def setup(bot) -> None:
    await bot.add_cog(GeneralCommands(bot))
