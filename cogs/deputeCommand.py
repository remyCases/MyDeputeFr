# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
import json
import discord
from discord.ext import commands
from discord.ext.commands import Context
from config.config import ACTEUR_FOLDER, SCRUTINS_FOLDER

from utils.deputeManager import Depute
from utils.scrutinManager import ResultBallot, Scrutin


class DeputeCommand(commands.Cog, name="depute"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="debugd",
        description="Commande de débogage pour afficher toutes les informations de débogage concernant un député.",
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
            description=f"Je n'ai pas trouvé le député {name}.",
            color=0x367588,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="debugs",
        description="Commande de débogage pour afficher toutes les informations de débogage concernant un scrutin.",
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
            description=f"Je n'ai pas trouvé le scrutin {code_ref}.",
            color=0x367588,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="nom",
        description="Affiche les informations d'un député en fonction de son nom.",
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
            with open(os.path.join(ACTEUR_FOLDER, file), "r") as f:
                data = json.load(f)

                if depute := Depute.from_json_by_name(data, name):
                    embed = discord.Embed(
                        title="Député",
                        description=depute.to_string(),
                        color=0x367588,
                    )
                    await context.send(embed=embed)
                    return
        
        embed = discord.Embed(
            title="Député",
            description=f"Je n'ai pas trouvé le député {name}.",
            color=0x367588,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="circo",
        description="Affiche les informations du député associé à une circonscription.",
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
            with open(os.path.join(ACTEUR_FOLDER, file), "r") as f:
                data = json.load(f)
                if depute := Depute.from_json_by_circo(data, code_dep, code_circo):
                    embed = discord.Embed(
                        title="Député",
                        description=depute.to_string(),
                        color=0x367588,
                    )
                    await context.send(embed=embed)
                    return
        
        embed = discord.Embed(
            title="Député",
            description=f"Je n'ai pas trouvé de député dans le {code_dep}-{code_circo}.",
            color=0x367588,
        )
        await context.send(embed=embed)

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

        description = ""
        for file in os.listdir(ACTEUR_FOLDER):
            with open(os.path.join(ACTEUR_FOLDER, file), "r") as f:
                data = json.load(f)
                if depute := Depute.from_json_by_dep(data, code_dep):
                    description += f"\n{depute.to_string_less()}."

        if description:
            embed = discord.Embed(
                title="Députés",
                description=description,
                color=0x367588,
            )
            await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Députés",
                description=f"Je n'ai pas trouvé de députés dans le département {code_dep}.",
                color=0x367588,
            )
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="vote",
        description="Affiche le vote d'un député pour un scrutin donné.",
    )
    async def vote(self, context: Context, name: str, code_ref: str) -> None:
        """
        TODO
        """

        for file_depute in os.listdir(ACTEUR_FOLDER):
            with open(os.path.join(ACTEUR_FOLDER, file_depute), "r") as f:
                data_depute = json.load(f)
                if depute := Depute.from_json_by_name(data_depute, name):

                    for file_scrutin in os.listdir(SCRUTINS_FOLDER):
                        with open(os.path.join(SCRUTINS_FOLDER, file_scrutin), "r") as g:
                            data_scrutin = json.load(g)
                            if scrutin := Scrutin.from_json_by_ref(data_scrutin, code_ref):
                            
                                embed = discord.Embed(
                                    title="Députés",
                                    description=scrutin.to_string_depute(depute),
                                    color=0x367588,
                                )
                                await context.send(embed=embed)
                                return
            
        embed = discord.Embed(
            title="Députés",
            description=f"Je n'ai pas trouvé le député {name} ou le scrutin {code_ref}.",
            color=0x367588,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="stat",
        description="Affiche les statistiques de vote d'un député.",
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
            with open(os.path.join(ACTEUR_FOLDER, file_depute), "r") as f:
                data_depute = json.load(f)
                if depute := Depute.from_json_by_name(data_depute, name):

                    for file_scrutin in os.listdir(SCRUTINS_FOLDER):
                        with open(os.path.join(SCRUTINS_FOLDER, file_scrutin), "r") as g:
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
                        title="Députés",
                        description=f"{depute.to_string_less()}\n{stat}",
                        color=0x367588,
                    )
                    await context.send(embed=embed)
                    return
 
        embed = discord.Embed(
            title="Députés",
            description=f"Je n'ai pas trouvé le député {name}.",
            color=0x367588,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
    name="scr",
    description="Affiche les informations d'un scrutin en fonction de son code de référence.",
    )
    async def scr(self, context: Context, code_ref: str) -> None:
        """
        TODO
        """

        for file in os.listdir(SCRUTINS_FOLDER):
            with open(os.path.join(SCRUTINS_FOLDER, file), "r") as f:
                data = json.load(f)
                if scrutin := Scrutin.from_json_by_ref(data, code_ref):
                    embed = discord.Embed(
                        title="Scrutin",
                        description=scrutin.to_string(),
                        color=0x367588,
                    )
                    await context.send(embed=embed)
                    return

        embed = discord.Embed(
            title="Scrutin",
            description=f"Je n'ai pas trouvé le scrutin {code_ref}.",
            color=0x367588,
        )
        await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(DeputeCommand(bot))
