# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from datetime import datetime
from typing import List, Optional
import discord
from discord.ext.commands import Context

from config.config import ACTEUR_FOLDER, SCRUTINS_FOLDER
from handlers.commonHandler import error_handler
from handlers.deputeHandler import vote_by_ref_handler
from utils.cogManager import ProtectedCog
from utils.commandManager import protected_command
from utils.deputeManager import Depute
from utils.scrutinManager import Scrutin
from utils.utils import read_files_from_directory

MIN_DATE_CURRENT_MOTION = datetime(2023, 1, 1).date()


class NotificationCommands(ProtectedCog):
    @protected_command(
        name="sub",
        description="TODO"
    )
    async def sub(self, context: Context, last_name: str, first_name: Optional[str] = None) -> None:

        deputes: List[Depute] = [
            depute
            for data in read_files_from_directory(ACTEUR_FOLDER)
            if (depute := Depute.from_json_by_name(data, last_name, first_name))
        ]

        for depute in deputes:
            result :bool = await self.bot.database.add_notification(
                context.author.id, context.guild.id, depute.ref
            )

            if result:
                description=f"**{context.author}** wants notifications for {depute.last_name} {depute.first_name}."
            else:
                description=f"**{context.author}** has already notifications for {depute.last_name} {depute.first_name}."

            embed = discord.Embed(
                description=description,
                color=0xBEBEFE,
            )

            await context.send(embed=embed)

    @protected_command(
        name="unsub",
        description="TODO"
    )
    async def unsub(self, context: Context, last_name: Optional[str] = None, first_name: Optional[str] = None) -> None:

        if last_name:
            deputes: List[Depute] = [
                depute
                for data in read_files_from_directory(ACTEUR_FOLDER)
                if (depute := Depute.from_json_by_name(data, last_name, first_name))
            ]
            for depute in deputes:
                await self.bot.database.remove_notifications(
                    context.author.id, context.guild.id, depute.ref
                )
                embed = discord.Embed(
                    description=f"**{context.author}** removes notifications for {depute.last_name} {depute.first_name}.",
                    color=0xBEBEFE,
                )
                await context.send(embed=embed)
        else:
            await self.bot.database.remove_notifications(
                context.author.id, context.guild.id
            )
            embed = discord.Embed(
                description=f"**{context.author}** removes all notifications.",
                color=0xBEBEFE,
            )
            await context.send(embed=embed)

    @protected_command(
        name="rcv",
        description="TODO"
    )
    async def rcv(self, context: Context) -> None:

        ref_notifs: List[str] = await self.bot.database.get_notifications(
            context.author.id, context.guild.id
        )

        if not ref_notifs:
            await context.send(embed=error_handler(
                description=f"{context.author.name} n'est inscrit à aucun député."
            ))

        last_scrutin_date = MIN_DATE_CURRENT_MOTION
        scrutins: List[Scrutin] = []
        for data in read_files_from_directory(SCRUTINS_FOLDER):
            scrutin = Scrutin.from_json(data)
            if scrutin.dateScrutin > last_scrutin_date:
                last_scrutin_date = scrutin.dateScrutin
                scrutins = [scrutin]
            elif scrutin.dateScrutin == last_scrutin_date:
                scrutins.append(scrutin)

        for ref in ref_notifs:
            embeds: List[discord.Embed] = vote_by_ref_handler(scrutins, ref)
            for embed in embeds:
                await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(NotificationCommands(bot))
