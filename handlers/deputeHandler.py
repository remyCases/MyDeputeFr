# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
import  json

import discord

from config.config import SCRUTINS_FOLDER, ACTEUR_FOLDER
from utils.deputeManager import Depute
from utils.scrutinManager import Scrutin, ResultBallot


def nom_handler(name: str) -> discord.Embed:
    for file in os.listdir(ACTEUR_FOLDER):
        with open(os.path.join(ACTEUR_FOLDER, file), "r") as f:
            data = json.load(f)

            if depute := Depute.from_json_by_name(data, name):
                return discord.Embed(
                    title="Député",
                    description=depute.to_string(),
                    color=0x367588,
                )

    return discord.Embed(
        title="Député",
        description=f"J'ai pas trouvé le député {name}.",
        color=0x367588,
    )


def ciro_handler(code_dep: str, code_circo: str) -> discord.Embed:
    for file in os.listdir(ACTEUR_FOLDER):
        with open(os.path.join(ACTEUR_FOLDER, file), "r") as f:
            data = json.load(f)
            if depute := Depute.from_json_by_circo(data, code_dep, code_circo):
                return discord.Embed(
                    title="Député",
                    description=depute.to_string(),
                    color=0x367588,
                )

    return discord.Embed(
        title="Député",
        description=f"J'ai pas trouvé de député dans le {code_dep}-{code_circo}.",
        color=0x367588,
    )

def dep_handler(code_dep: str) -> discord.Embed:
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
    else:
        embed = discord.Embed(
            title="Députés",
            description=f"J'ai pas trouvé de députés dans le département {code_dep}.",
            color=0x367588,
        )
    return embed

def vote_handler(name: str, code_ref: str) -> discord.Embed :
    for file_depute in os.listdir(ACTEUR_FOLDER):
        with open(os.path.join(ACTEUR_FOLDER, file_depute), "r") as f:
            data_depute = json.load(f)
            if depute := Depute.from_json_by_name(data_depute, name):

                for file_scrutin in os.listdir(SCRUTINS_FOLDER):
                    with open(os.path.join(SCRUTINS_FOLDER, file_scrutin), "r") as g:
                        data_scrutin = json.load(g)
                        if scrutin := Scrutin.from_json_by_ref(data_scrutin, code_ref):
                            return discord.Embed(
                                title="Députés",
                                description=scrutin.to_string_depute(depute),
                                color=0x367588,
                            )

    return discord.Embed(
        title="Députés",
        description=f"J'ai pas trouvé le député {name} ou le scrutin {code_ref}.",
        color=0x367588,
    )


def stat_handler(name:str) -> discord.Embed:
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

                return discord.Embed(
                    title="Députés",
                    description=f"{depute.to_string_less()}\n{stat}",
                    color=0x367588,
                )


    return discord.Embed(
        title="Députés",
        description=f"J'ai pas trouvé le député {name}.",
        color=0x367588,
    )


def scr_handler(code_ref: str) -> discord.Embed:
    for file in os.listdir(SCRUTINS_FOLDER):
        with open(os.path.join(SCRUTINS_FOLDER, file), "r") as f:
            data = json.load(f)
            if scrutin := Scrutin.from_json_by_ref(data, code_ref):
                return discord.Embed(
                    title="Scrutin",
                    description=scrutin.to_string(),
                    color=0x367588,
                )

    return discord.Embed(
        title="Scrutin",
        description=f"J'ai pas trouvé le scrutin {code_ref}.",
        color=0x367588,
    )

