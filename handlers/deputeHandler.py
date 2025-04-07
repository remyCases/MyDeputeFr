# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
import json

import discord
from discord import Embed

from config.config import SCRUTINS_FOLDER, ACTEUR_FOLDER
from utils.deputeManager import Depute
from utils.scrutinManager import Scrutin, ResultBallot


def error_handler(title: str = "Erreur", description: str = "Une erreur inconnue est survenu", color=0x367588) -> discord.Embed:
    """
    Return a generic error embed message.

    Parameters:
        title (str): Embed title.
        description (str): Error description.
        color (int): Color of the embed.

    Returns:
        discord.Embed: The error message embed.
    """
    return discord.Embed(
        title=title,
        description=description,
        color=color,
    )


def nom_handler(name: str) -> Embed:
    """
    Return embed with député info based on name.

    Parameters:
        name (str): The name of the député.

    Returns:
        discord.Embed: Embed containing député info or error message.
    """
    for file in os.listdir(ACTEUR_FOLDER):
        with open(os.path.join(ACTEUR_FOLDER, file), "r") as f:
            data = json.load(f)

            if depute := Depute.from_json_by_name(data, name):
                embed = discord.Embed(
                    title=f"{depute.first_name} {depute.last_name}",
                    description=depute.to_string(),
                    color=0x367588,
                    url=depute.url
                )
                embed.set_thumbnail(url=depute.image)
                return embed
    return error_handler(description=f"J'ai pas trouvé le député {name}.")


def ciro_handler(code_dep: str, code_circo: str) -> discord.Embed:
    """
    Return embed with député info from a specific circonscription.

    Parameters:
        code_dep (str): Department code.
        code_circo (str): Circonscription code.

    Returns:
        discord.Embed: Embed with député info or error.
    """
    for file in os.listdir(ACTEUR_FOLDER):
        with open(os.path.join(ACTEUR_FOLDER, file), "r") as f:
            data = json.load(f)
            if depute := Depute.from_json_by_circo(data, code_dep, code_circo):
                embed = discord.Embed(
                    title=f"{depute.first_name} {depute.last_name}",
                    description=depute.to_string(),
                    color=0x367588,
                    url=depute.url
                )
                embed.set_thumbnail(url=depute.image)
                return embed

    return error_handler(description=f"J'ai pas trouvé de député dans le {code_dep}-{code_circo}.")


def dep_handler(code_dep: str) -> discord.Embed:
    """
    Return embed listing all députés from a department.

    Parameters:
        code_dep (str): Department code.

    Returns:
        discord.Embed: Embed with list of députés or error.
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
        return embed
    return error_handler(description=f"J'ai pas trouvé de députés dans le département {code_dep}.")


def vote_handler(name: str, code_ref: str) -> discord.Embed:
    """
    Return embed showing how a député voted in a scrutin.

    Parameters:
        name (str): The name of the député.
        code_ref (str): Reference of the scrutin.

    Returns:
        discord.Embed: Embed showing the voting result or error.
    """
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
    return error_handler(description=f"J'ai pas trouvé le député {name} ou le scrutin {code_ref}.")


def stat_handler(name: str) -> discord.Embed:
    """
    Return embed with voting statistics for a député.

    Parameters:
        name (str): The name of the député.

    Returns:
        discord.Embed: Embed showing statistics or error.
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

                return discord.Embed(
                    title="Députés",
                    description=f"{depute.to_string_less()}\n{stat}",
                    color=0x367588,
                )
    return error_handler(description=f"J'ai pas trouvé le député {name}.")


def scr_handler(code_ref: str) -> discord.Embed:
    """
    Return embed with information about a scrutin.

    Parameters:
        code_ref (str): Reference of the scrutin.

    Returns:
        discord.Embed: Embed with scrutin info or error.
    """
    for file in os.listdir(SCRUTINS_FOLDER):
        with open(os.path.join(SCRUTINS_FOLDER, file), "r") as f:
            data = json.load(f)
            if scrutin := Scrutin.from_json_by_ref(data, code_ref):
                return discord.Embed(
                    title="Scrutin",
                    description=scrutin.to_string(),
                    color=0x367588,
                )
    return error_handler(description=f"J'ai pas trouvé le scrutin {code_ref}.")
