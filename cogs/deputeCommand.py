# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
import json
from getopt import error
from typing import Self
import discord

from discord.ext import commands
from discord.ext.commands import Context

from handlers.deputeHandler import scr_handler, stat_handler, vote_handler, dep_handler, ciro_handler, nom_handler
from config.config import ACTEUR_FOLDER, SCRUTINS_FOLDER

from utils.cogManager import ProtectedCog
from utils.commandManager import protected_command
from utils.utils import MODE
from utils.deputeManager import Depute
from utils.scrutinManager import ResultBallot, Scrutin


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


class DeputeCommand(ProtectedCog, name="depute"):
    """
    Cog that manages commands related to members of parliament (députés).
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
        for file in os.listdir(ACTEUR_FOLDER):
            with open(os.path.join(ACTEUR_FOLDER, file), "r", encoding="utf-8") as f:
                data = json.load(f)

                if depute := Depute.from_json_by_name(data, name):
                    embed = discord.Embed(
                        title=f"{depute.first_name} {depute.last_name}",
                        description=depute,
                        color=0x367588,
                    )
                    await context.send(embed=embed)
                    return

        embed = discord.Embed(
            title="Erreur",
            description=f"J'ai pas trouvé le député {name}.",
            color=0x367588,
        )
        await context.send(embed=embed)

    @protected_command(
        name="debugs",
        description="Debug command.",
    )
    @debug_command()
    async def debugs(self, context: Context, code_ref: str) -> None:
        """
        Show debug info for a scrutin by code reference.

        Parameters:
            context (Context): The context of the command.
            code_ref (str): The reference code of the scrutin.
        """
        for file in os.listdir(SCRUTINS_FOLDER):
            with open(os.path.join(SCRUTINS_FOLDER, file), "r", encoding="utf-8") as f:
                data = json.load(f)

                if scrutin := Scrutin.from_json_by_ref(data, code_ref):
                    embed = discord.Embed(
                        title=f"Scrutin nº{scrutin.ref}",
                        description=scrutin,
                        color=0x367588,
                    )
                    await context.send(embed=embed)
                    return

        embed = discord.Embed(
            title="Erreur",
            description=f"J'ai pas trouvé le scrutin {code_ref}.",
            color=0x367588,
        )
        await context.send(embed=embed)

    @protected_command(
        name="nom",
        description="Affiche un député.",
    )
    async def nom(self, context: Context, name: str) -> None:
        """
        Display a député's info by name.

        Parameters:
            context (Context): The context of the command.
            name (str): The name of the député.
        """
        await context.send(embed=nom_handler(name))

    @protected_command(
        name="circo",
        description="Affiche le député associé à une circonscription.",
    )
    async def circo(self, context: Context, code_dep: str, code_circo: str) -> None:
        """
        Display a député by department and circonscription.

        Parameters:
            context (Context): The context of the command.
            code_dep (str): Department code.
            code_circo (str): Circonscription code.
        """
        await context.send(embed=ciro_handler(code_dep, code_circo))

    @protected_command(
        name="dep",
        description="Affiche la liste des députés dans un département.",
    )
    async def dep(self, context: Context, code_dep: str) -> None:
        """
        Display députés for a given department.

        Parameters:
            context (Context): The context of the command.
            code_dep (str): Department code.
        """
        await context.send(embed=dep_handler(code_dep))

    @commands.hybrid_command(
        name="vote",
        description="TODO",
    )
    async def vote(self, context: Context, name: str, code_ref: str) -> None:
        """
        Display how a député voted in a scrutin.

        Parameters:
            context (Context): The context of the command.
            name (str): Name of the député.
            code_ref (str): Reference of the scrutin.
        """
        await context.send(embed=vote_handler(name, code_ref))

    @commands.hybrid_command(
        name="stat",
        description="TODO",
    )
    async def stat(self, context: Context, name: str) -> None:
        """
        Display voting statistics for a député.

        Parameters:
            context (Context): The context of the command.
            name (str): Name of the député.
        """
        await context.send(embed=stat_handler(name))

    @protected_command(
        name="scr",
        description="TODO",
    )
    async def scr(self, context: Context, code_ref: str) -> None:
        """
        Display info about a scrutin.

        Parameters:
            context (Context): The context of the command.
            code_ref (str): Reference of the scrutin.
        """
        await context.send(embed=scr_handler(code_ref))


async def setup(bot) -> None:
    """
    Setup function to add DeputeCommand cog to bot.

    Parameters:
        bot: The Discord bot instance.
    """
    await bot.add_cog(DeputeCommand(bot))
