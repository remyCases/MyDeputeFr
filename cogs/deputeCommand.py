# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
import json
import discord
from discord.ext import commands
from discord.ext.commands import Context

from cogs.utils.deputeManager import Depute
from cogs.utils.scrutinManager import Scrutin

ACTEUR_FOLDER = "acteur"
SCRUTINS_FOLDER = "Scrutins\\json"

class DeputeCommand(commands.Cog, name="depute"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="debug",
        description="Debug command.",
    )
    async def debug(self, context: Context, name: str) -> None:
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
                        description=depute.to_string_debug(),
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
            description=f"J'ai pas trouvé le député {name}.",
            color=0x367588,
        )
        await context.send(embed=embed)

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
            description=f"J'ai pas trouvé de député dans le {code_dep}-{code_circo}.",
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
                description=f"J'ai pas trouvé de députés dans le département {code_dep}.",
                color=0x367588,
            )
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="vote",
        description="TODO",
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
                            ref: str = data_scrutin["scrutin"]["numero"]
                            if ref != code_ref:
                                continue

                            scrutin = Scrutin.from_json(data_scrutin)
                            groupes = data_scrutin["scrutin"]["ventilationVotes"]["organe"]["groupes"]["groupe"]
                            res = ""
                            for groupe in groupes:
                                organe_ref = groupe["organeRef"]
                                if organe_ref != depute.gp_ref:
                                    continue

                                nonVotants = groupe["vote"]["decompteNominatif"]["nonVotants"]
                                if nonVotants:
                                    nonVotants = nonVotants["votant"]
                                    if isinstance(nonVotants, list):
                                        for nonVotant in nonVotants:
                                            if nonVotant["acteurRef"] != depute.ref:
                                                continue
                                            res = "non votant"
                                            break
                                    else:
                                        if nonVotants["acteurRef"] == depute.ref:
                                            res = "non votant"

                                if res: break

                                pours = groupe["vote"]["decompteNominatif"]["pours"]
                                if pours:
                                    pours = pours["votant"]
                                    if isinstance(pours, list):
                                        for pour in pours:
                                            if pour["acteurRef"] != depute.ref:
                                                continue
                                            res = "pour"
                                            break
                                    else:
                                        if pours["acteurRef"] == depute.ref:
                                            res = "pour"

                                if res: break

                                contres = groupe["vote"]["decompteNominatif"]["contres"]
                                if contres:
                                    contres = contres["votant"]
                                    if isinstance(contres, list):
                                        for contre in contres:
                                            if contre["acteurRef"] != depute.ref:
                                                continue
                                            res = "contre"
                                            break
                                    else:
                                        if contres["acteurRef"] == depute.ref:
                                            res = "contre"

                                if res: break

                                abstentions = groupe["vote"]["decompteNominatif"]["abstentions"]
                                if abstentions:
                                    abstentions = abstentions["votant"]
                                    if isinstance(abstentions, list):
                                        for abstention in abstentions:
                                            if abstention["acteurRef"] != depute.ref:
                                                continue
                                            res = "abstention"
                                            break
                                    else:
                                        if abstentions["acteurRef"] == depute.ref:
                                            res = "abstention"
                                break

                            if not res: res = "absent"

                            embed = discord.Embed(
                                title="Députés",
                                description=scrutin.to_string_depute(depute, res),
                                color=0x367588,
                            )
                            await context.send(embed=embed)
                            return
            
        embed = discord.Embed(
            title="Députés",
            description=f"J'ai pas trouvé le député {name} ou le scrutin {code_ref}.",
            color=0x367588,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
    name="scr",
    description="TODO",
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
            description=f"J'ai pas trouvé le scrutin {code_ref}.",
            color=0x367588,
        )
        await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(DeputeCommand(bot))
