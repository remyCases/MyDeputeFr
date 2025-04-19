# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.
from __future__ import annotations

import discord
from discord import Embed

from config.config import SCRUTINS_FOLDER, ACTEUR_FOLDER, DISCORD_EMBED_COLOR_MSG
from handlers.commonHandler import error_handler
from utils.deputeManager import Depute
from utils.scrutinManager import Scrutin, ResultBallot
from utils.utils import read_files_from_directory


def nom_handler(name: str) -> Embed:
    """
    Return embed with député info based on name.

    Parameters:
        name (str): The name of the député.

    Returns:
        discord.Embed: Embed containing député info or error message.
    """
    for data in read_files_from_directory(ACTEUR_FOLDER):
        if depute := Depute.from_json_by_name(data, name):
            embed = discord.Embed(
                title=f"{depute.first_name} {depute.last_name}",
                description=f"{depute.to_string()}",
                color=DISCORD_EMBED_COLOR_MSG,
                url=depute.url
            )
            embed.set_thumbnail(url=depute.image)
            return embed
    return error_handler(description=f"Je n'ai pas trouvé le député {name}.")



def ciro_handler(code_dep: str, code_circo: str) -> discord.Embed:
    """
    Return embed with député info from a specific circonscription.

    Parameters:
        code_dep (str): Department code.
        code_circo (str): Circonscription code.

    Returns:
        discord.Embed: Embed with député info or error.
    """
    for data in read_files_from_directory(ACTEUR_FOLDER):
        if depute := Depute.from_json_by_circo(data, code_dep, code_circo):
            embed = discord.Embed(
                title=f"{depute.first_name} {depute.last_name}",
                description=f"{depute.to_string()}",
                color=DISCORD_EMBED_COLOR_MSG,
                url=depute.url
            )
            embed.set_thumbnail(url=depute.image)
            return embed

    return error_handler(description=f"Je n'ai pas trouvé de député dans le {code_dep}-{code_circo}.")


def dep_handler(code_dep: str) -> discord.Embed:
    """
    Return embed listing all députés from a department.

    Parameters:
        code_dep (str): Department code.

    Returns:
        discord.Embed: Embed with list of députés or error.
    """
    description = ""
    for data in read_files_from_directory(ACTEUR_FOLDER):
        if depute := Depute.from_json_by_dep(data, code_dep):
            description += f"\n{depute.to_string()}"

    if description:
        embed = discord.Embed(
            title=f"Département {code_dep}",
            description=description,
            color=DISCORD_EMBED_COLOR_MSG,
        )
        return embed
    return error_handler(description=f"Je n'ai pas trouvé de députés dans le département {code_dep}.")


def vote_handler(name: str, code_ref: str) -> discord.Embed:
    """
    Return embed showing how a député voted in a scrutin.

    Parameters:
        name (str): The name of the député.
        code_ref (str): Reference of the scrutin.

    Returns:
        discord.Embed: Embed showing the voting result or error.
    """
    depute : Depute | None =  next(
        (depute for x in read_files_from_directory(ACTEUR_FOLDER) if (depute := Depute.from_json_by_name(x, name))),
        None
    )
    scrutin : Scrutin | None = next(
        (scrutin for x in read_files_from_directory(SCRUTINS_FOLDER) if (scrutin := Scrutin.from_json_by_ref(x, code_ref))),
        None
    )
    if scrutin and depute:
        embed = discord.Embed(
            title=f"{':green_circle:' if scrutin.sort == 'adopté' else ':red_circle:'}  Scrutin nº{scrutin.ref} - {depute.first_name} {depute.last_name} ",
            description=scrutin.to_string_depute(depute),
            color=DISCORD_EMBED_COLOR_MSG,
        )
        embed.set_thumbnail(url=depute.image)
        return embed
    elif scrutin:
        return error_handler(description=f"Je n'ai pas trouvé le député {name}.")
    elif depute:
        return error_handler(description=f"Je n'ai pas trouvé le scrutin {code_ref}.")
    else:
        return error_handler(description=f"Je n'ai trouvé ni le député {name}, ni le scrutin {code_ref}.")



def stat_handler(name: str) -> discord.Embed:
    """
    Return embed with voting statistics for a député.

    Parameters:
        name (str): The name of the député.

    Returns:
        discord.Embed: Embed showing statistics or error.
    """
    def update_stat(p_stat: dict[str, int], p_scrutin: Scrutin, p_depute:Depute) :
        result = p_scrutin.result(p_depute)

        if result == ResultBallot.ABSENT:
            p_stat["absent"] += 1
        elif result == ResultBallot.NONVOTANT:
            p_stat["nonvotant"] += 1
        elif result == ResultBallot.POUR:
            p_stat["pour"] += 1
        elif result == ResultBallot.CONTRE:
            p_stat["contre"] += 1
        elif result == ResultBallot.ABSTENTION:
            p_stat["abstention"] += 1

    stat = {
        "absent": 0,
        "nonvotant": 0,
        "pour": 0,
        "contre": 0,
        "abstention": 0,
    }

    for data_depute in read_files_from_directory(ACTEUR_FOLDER):
        if depute := Depute.from_json_by_name(data_depute, name):
            for data_scrutin in read_files_from_directory(SCRUTINS_FOLDER):
                scrutin = Scrutin.from_json(data_scrutin)
                update_stat(stat, scrutin, depute)
            embed= discord.Embed(
                title=f"{depute.first_name} {depute.last_name}",
                description=f"{depute.to_string()[:-1]}: {stat}",
                color=DISCORD_EMBED_COLOR_MSG,
                url=depute.url
            )
            embed.set_thumbnail(url=depute.image)
            return embed
    return error_handler(description=f"Je n'ai pas trouvé le député {name}.")


def scr_handler(code_ref: str) -> discord.Embed:
    """
    Return embed with information about a scrutin.

    Parameters:
        code_ref (str): Reference of the scrutin.

    Returns:
        discord.Embed: Embed with scrutin info or error.
    """
    for data in read_files_from_directory(SCRUTINS_FOLDER):
        if scrutin := Scrutin.from_json_by_ref(data, code_ref):
            embed = discord.Embed(
                title=f"{':green_circle:' if scrutin.sort == 'adopté' else ':red_circle:'} Scrutin nº{scrutin.ref}",
                description=f"Le {scrutin.dateScrutin}, {scrutin.titre[:-1]} est {scrutin.sort}.\n",
                color=DISCORD_EMBED_COLOR_MSG,
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
            return embed
    return error_handler(description=f"Je n'ai pas trouvé le scrutin {code_ref}.")
