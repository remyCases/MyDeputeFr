# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
import json
import discord

from discord.ext import commands
from discord.ext.commands import Context

from handlers.deputeHandler import scr_handler, stat_handler, vote_handler, dep_handler, ciro_handler, nom_handler
from config.config import ACTEUR_FOLDER, SCRUTINS_FOLDER

from utils.deputeManager import Depute
from utils.scrutinManager import ResultBallot, Scrutin


class DeputeCommand(commands.Cog, name="depute"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="debugd",
        description="Debug command.",
    )
    async def debugd(self, context: Context, name: str) -> None:
        """
        This is a debug command that displays all debug information regarding a member of parliament.

        ----------
        context: Context
            The application command context.
        name: str
            Name of a member of parliament
        """

        for file in os.listdir(ACTEUR_FOLDER):
            with open(os.path.join(ACTEUR_FOLDER, file), "r") as f:
                data = json.load(f)

                if depute := Depute.from_json_by_name(data, name):
                    embed = discord.Embed(
                        title="Député",
                        description=depute,
                        color=0x367588,
                    )
                    await context.send(embed=embed)
                    return
        
        embed = discord.Embed(
            title="Député",
            description=f"J'ai pas trouvé le député {name}.",
            color=0x367588,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="debugs",
        description="Debug command.",
    )
    async def debugs(self, context: Context, code_ref: str) -> None:
        """
        TODO

        ----------
        context: Context
            The application command context.
        code_ref: str
            Code of a ballot
        """

        for file in os.listdir(SCRUTINS_FOLDER):
            with open(os.path.join(SCRUTINS_FOLDER, file), "r") as f:
                data = json.load(f)

                if scrutin := Scrutin.from_json_by_ref(data, code_ref):
                    embed = discord.Embed(
                        title="Scrutin",
                        description=scrutin,
                        color=0x367588,
                    )
                    await context.send(embed=embed)
                    return
        
        embed = discord.Embed(
            title="Scrutin",
            description=f"J'ai pas trouvé le scrutin {code_ref}.",
            color=0x367588,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="nom",
        description="Affiche un député.",
    )
    async def nom(self, context: Context, name: str) -> None:
        """
        Display information about a member of parliament given its name.

        ----------
        context: Context
            The application command context.
        name: str
            Name of a member of parliament
        """
        await context.send(embed=nom_handler(name))

    @commands.hybrid_command(
        name="circo",
        description="Affiche le député associé à une circonscription.",
    )
    async def circo(self, context: Context, code_dep: str, code_circo: str) -> None:
        """
        Display information about a member of parliament given an administrative subdivision

        ----------
        context: Context
            The application command context.
        dep: str
            Administrative division
        circo: str
            Administrative subdivision
        """


        await context.send(embed=ciro_handler(code_dep,code_circo))

    @commands.hybrid_command(
        name="dep",
        description="Affiche la liste des députés dans un département.",
    )
    async def dep(self, context: Context, code_dep: str) -> None:
        """
        Display information about a list of members of parliament given an administrative division

        ----------
        context: Context
            The application command context.
        dep: str
            Administrative division
        """
        await context.send(embed=dep_handler(code_dep))

    @commands.hybrid_command(
        name="vote",
        description="TODO",
    )
    async def vote(self, context: Context, name: str, code_ref: str) -> None:
        """
        TODO
        """
        await context.send(embed=vote_handler(name, code_ref))

    @commands.hybrid_command(
        name="stat",
        description="TODO",
    )
    async def stat(self, context: Context, name: str) -> None:
        """
        TODO
        """
        await context.send(embed=stat_handler(name))

    @commands.hybrid_command(
    name="scr",
    description="TODO",
    )
    async def scr(self, context: Context, code_ref: str) -> None:
        """
        TODO
        """
        await context.send(embed=scr_handler(code_ref))


async def setup(bot) -> None:
    await bot.add_cog(DeputeCommand(bot))
