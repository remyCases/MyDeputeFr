# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
import json
from typing import Self
import discord
from discord.ext import commands
from discord.ext.commands import Context
from config.config import ACTEUR_FOLDER, SCRUTINS_FOLDER

from utils.cogManager import ProtectedCog
from utils.commandManager import protected_command
from utils.utils import MODE
from utils.deputeManager import Depute
from utils.scrutinManager import ResultBallot, Scrutin

def debug_command():
    """
    Decorator for debug commands, will check if the bot is in DEBUG mode.
    Else will return a message to the user indicating the command is not available.
    """
    async def predicate(ctx: Context):
        if ctx.bot.mode != MODE.DEBUG:
            await ctx.send("Commande non disponible en mode release.")
            return False
        return True
    return commands.check(predicate)

class DeputeCommand(ProtectedCog, name="depute"):
    @protected_command(
        name="debugd",
        description="Debug command.",
    )
    @debug_command()
    async def debugd(self: Self, context: Context, name: str) -> None:
        """
        This is a debug command that displays all debug information regarding a member of parliament.

        ----------
        context: Context
            The application command context.
        name: str
            Name of a member of parliament
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
        TODO

        ----------
        context: Context
            The application command context.
        code_ref: str
            Code of a ballot
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
        Display information about a member of parliament given its name.

        ----------
        context: Context
            The application command context.
        name: str
            Name of a member of parliament
        """

        for file in os.listdir(ACTEUR_FOLDER):
            with open(os.path.join(ACTEUR_FOLDER, file), "r", encoding="utf-8") as f:
                data = json.load(f)

                if depute := Depute.from_json_by_name(data, name):
                    embed = discord.Embed(
                        title=f"{depute.first_name} {depute.last_name}",
                        description=depute.to_string(),
                        color=0x367588,
                        url=depute.url
                    )
                    embed.set_thumbnail(url=depute.image)
                    await context.send(embed=embed)
                    return

        embed = discord.Embed(
            title="Erreur",
            description=f"J'ai pas trouvé le député {name}.",
            color=0x367588,
        )
        await context.send(embed=embed)

    @protected_command(
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

        for file in os.listdir(ACTEUR_FOLDER):
            with open(os.path.join(ACTEUR_FOLDER, file), "r", encoding="utf-8") as f:
                data = json.load(f)
                if depute := Depute.from_json_by_circo(data, code_dep, code_circo):
                    embed = discord.Embed(
                        title=f"{depute.first_name} {depute.last_name}",
                        description=depute.to_string(),
                        color=0x367588,
                        url=depute.url
                    )
                    embed.set_thumbnail(url=depute.image)
                    await context.send(embed=embed)
                    return
        
        embed = discord.Embed(
            title="Erreur",
            description=f"J'ai pas trouvé de député dans le {code_dep}-{code_circo}.",
            color=0x367588,
        )
        await context.send(embed=embed)

    @protected_command(
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

        description = ""
        for file in os.listdir(ACTEUR_FOLDER):
            with open(os.path.join(ACTEUR_FOLDER, file), "r", encoding="utf-8") as f:
                data = json.load(f)
                if depute := Depute.from_json_by_dep(data, code_dep):
                    description += f"\n{depute.to_string_less()}."

        if description:
            embed = discord.Embed(
                title=f"Département {code_dep}",
                description=description,
                color=0x367588,
            )
            await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Erreur",
                description=f"J'ai pas trouvé de députés dans le département {code_dep}.",
                color=0x367588,
            )
            await context.send(embed=embed)

    @protected_command(
        name="vote",
        description="TODO",
    )
    async def vote(self, context: Context, name: str, code_ref: str) -> None:
        """
        TODO
        """

        for file_depute in os.listdir(ACTEUR_FOLDER):
            with open(os.path.join(ACTEUR_FOLDER, file_depute), "r", encoding="utf-8") as f:
                data_depute = json.load(f)
                if depute := Depute.from_json_by_name(data_depute, name):

                    for file_scrutin in os.listdir(SCRUTINS_FOLDER):
                        with open(os.path.join(SCRUTINS_FOLDER, file_scrutin), "r", encoding="utf-8") as g:
                            data_scrutin = json.load(g)
                            if scrutin := Scrutin.from_json_by_ref(data_scrutin, code_ref):

                                embed = discord.Embed(
                                    title=f"{depute.first_name} {depute.last_name}",
                                    description=scrutin.to_string_depute(depute),
                                    color=0x367588,
                                )
                                await context.send(embed=embed)
                                return

        embed = discord.Embed(
            title="Erreur",
            description=f"J'ai pas trouvé le député {name} ou le scrutin {code_ref}.",
            color=0x367588,
        )
        await context.send(embed=embed)

    @protected_command(
        name="stat",
        description="TODO",
    )
    async def stat(self, context: Context, name: str) -> None:
        """
        TODO
        """
        stat = {
            "absent": 0,
            "nonvotant": 0,
            "pour": 0,
            "contre": 0,
            "abstention": 0,
        }

        for file_depute in os.listdir(ACTEUR_FOLDER):
            with open(os.path.join(ACTEUR_FOLDER, file_depute), "r", encoding="utf-8") as f:
                data_depute = json.load(f)
                if depute := Depute.from_json_by_name(data_depute, name):

                    for file_scrutin in os.listdir(SCRUTINS_FOLDER):
                        with open(os.path.join(SCRUTINS_FOLDER, file_scrutin), "r", encoding="utf-8") as g:
                            data_scrutin = json.load(g)
                            scrutin = Scrutin.from_json(data_scrutin)

                            match scrutin.result(depute):
                                case ResultBallot.ABSENT:
                                    stat["absent"] += 1
                                case ResultBallot.NONVOTANT:
                                    stat["nonvotant"] += 1
                                case ResultBallot.POUR:
                                    stat["pour"] += 1
                                case ResultBallot.CONTRE:
                                    stat["contre"] += 1
                                case ResultBallot.ABSTENTION:
                                    stat["abstention"] += 1

                    embed = discord.Embed(
                        title=f"{depute.first_name} {depute.last_name}",
                        description=f"{depute.to_string_less()}\n{stat}",
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
        name="scr",
        description="TODO",
    )
    async def scr(self, context: Context, code_ref: str) -> None:
        """
        TODO
        """

        for file in os.listdir(SCRUTINS_FOLDER):
            with open(os.path.join(SCRUTINS_FOLDER, file), "r", encoding="utf-8") as f:
                data = json.load(f)
                if scrutin := Scrutin.from_json_by_ref(data, code_ref):
                    embed = discord.Embed(
                        title=f"{':green_circle:' if scrutin.sort == 'adopté' else ':red_circle:'}  Scrutin nº{scrutin.ref} ",
                        description=f"Le {scrutin.dateScrutin}, {scrutin.titre[:-1]} est {scrutin.sort}.\n",
                        color=0x367588,
                    )
                    embed.add_field(
                        name="Participations",
                        value=
                        f":ballot_box: Nombre de votants: {scrutin.nombreVotants}\n"
                        f":exclamation: Non votants: {scrutin.nonVotant}\n"
                        f":no_entry_sign: Non votants volontaires: {scrutin.nonVotantsVolontaire}",
                        inline=True
                    )
                    embed.add_field(
                        name="Résulats",
                        value=
                        f":green_circle: Pour: {scrutin.pour}\n"
                        f":red_circle: Contre: {scrutin.contre}\n"
                        f":white_circle: Abstentions: {scrutin.abstention}",
                        inline=True
                    )
                    await context.send(embed=embed)
                    return

        embed = discord.Embed(
            title="Erreur",
            description=f"J'ai pas trouvé le scrutin {code_ref}.",
            color=0x367588,
        )
        await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(DeputeCommand(bot))
