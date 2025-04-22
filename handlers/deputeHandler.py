# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.
from __future__ import annotations

import discord

from config.config import SCRUTINS_FOLDER, ACTEUR_FOLDER, DISCORD_EMBED_COLOR_MSG
from handlers.commonHandler import error_handler
from utils.deputeManager import Depute
from utils.scrutinManager import Scrutin, ResultBallot
from utils.utils import read_files_from_directory


def __depute_to_embed(depute: Depute) -> discord.Embed:
    """
    Converts a Depute object into a Discord Embed message.

    Parameters:
        depute (Depute): The deputy object.

    Returns:
        discord.Embed: A Discord Embed formatted with the deputy's details.
    """
    return discord.Embed(
        title=f":bust_in_silhouette: {depute.first_name} {depute.last_name}",
        description=(
            f":round_pushpin: **Circoncription** : {depute.dep}-{depute.circo} ({depute.dep_name})\n"
            f":classical_building: **Groupe** : {depute.gp}"
        ),
        color=DISCORD_EMBED_COLOR_MSG,
        url=depute.url
    ).set_thumbnail(url=depute.image)


def nom_handler(last_name: str, first_name: str | None = None) -> list[discord.Embed]:
    """
    Retrieve embeds with député information based on the given name.

    Parameters:
        last_name (str): The last name of the député.
        first_name (str | None): The optional first name of the député.

    Returns:
        list[discord.Embed]: A list of embeds with député info or an error message.
    """
    deputes = [ depute for data in read_files_from_directory(ACTEUR_FOLDER)
                if (depute := Depute.from_json_by_name(data, last_name, first_name)) ]
    if len(deputes) > 0 :
        deputes.sort(key=lambda x: int(x.circo))
        return [
            __depute_to_embed(depute)
            for depute in deputes
        ]
    full_name = f"{first_name + ' ' if first_name else ''}{last_name}"
    return [ error_handler(
        title="Député non trouvé",
        description=f"Je n'ai pas trouvé le député {full_name}."
    ) ]


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
            return __depute_to_embed(depute)

    return error_handler(
        title="Député non trouvé",
        description=f"Je n'ai pas trouvé de député dans le {code_dep}-{code_circo}."
    )


def dep_handler(code_dep: str) -> discord.Embed:
    """
    Return embed listing all députés from a department.

    Parameters:
        code_dep (str): Department code.

    Returns:
        discord.Embed: Embed with list of députés or error.
    """
    deputes = [ depute for data in read_files_from_directory(ACTEUR_FOLDER)
                if (depute := Depute.from_json_by_dep(data, code_dep)) ]

    if len(deputes) > 0:
        deputes.sort(key=lambda x: int(x.circo))
        description = '\n'.join([
            f":bust_in_silhouette: [{depute.first_name} {depute.last_name}]({depute.url}) — "
            f":round_pushpin: **Circoncription** : {depute.dep}-{depute.circo} | "
            f":classical_building: **Groupe** : {depute.gp}"
            for depute in deputes
        ])
        return discord.Embed(
            title=f":pushpin: Département {deputes[0].dep} ({deputes[0].dep_name})",
            description=description,
            color=DISCORD_EMBED_COLOR_MSG,
        )

    return error_handler(title="Député non trouvé", description=f"Je n'ai pas trouvé de députés dans le département {code_dep}.")


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
        return error_handler(title="Député non trouvé", description=f"Je n'ai pas trouvé le député {name}.")
    elif depute:
        return error_handler(title="Scrutin non trouvé", description=f"Je n'ai pas trouvé le scrutin {code_ref}.")
    else:
        return error_handler(title="Député et scrutin non trouvé", description=f"Je n'ai trouvé ni le député {name}, ni le scrutin {code_ref}.")



def stat_handler(name: str) -> discord.Embed:
    """
    Return embed with voting statistics for a député.

    Parameters:
        name (str): The name of the député.

    Returns:
        discord.Embed: Embed showing statistics or error.
    """

    def update_stat(stat: dict[str, int], scrutin: Scrutin, depute: Depute):
        result = scrutin.result(depute)
        if result == ResultBallot.ABSENT:
            stat["absent"] += 1
        elif result == ResultBallot.NONVOTANT:
            stat["nonvotant"] += 1
        elif result == ResultBallot.POUR:
            stat["pour"] += 1
        elif result == ResultBallot.CONTRE:
            stat["contre"] += 1
        elif result == ResultBallot.ABSTENTION:
            stat["abstention"] += 1

    def emoticon_stat(k: str) -> str:
        return {
            "pour": ":green_circle:",
            "contre": ":red_circle:",
            "abstention": ":white_circle:",
            "nonvotant": ":exclamation:",
            "absent": ":orange_circle:",
        }.get(k, "")

    deputes = [
        depute
        for data in read_files_from_directory(ACTEUR_FOLDER)
        if (depute := Depute.from_json_by_name(data, last_name, first_name))
    ]

    if len(deputes) > 0:
        deputes.sort(key=lambda d: int(d.circo))

        default_stat = { "absent": 0, "pour": 0, "contre": 0, "abstention": 0, "nonvotant": 0}
        stats = {depute.ref: default_stat.copy() for depute in deputes}

        for data in read_files_from_directory(SCRUTINS_FOLDER):
            scrutin = Scrutin.from_json(data)
            for depute in deputes:
                update_stat(stats[depute.ref], scrutin, depute)

        embeds = []
        for depute in deputes:
            embed = __depute_to_embed(depute)
            stat_lines = "\n".join(f"{emoticon_stat(key) + ' ' if emoticon_stat(key) else ''}{key.capitalize()} : {value}" for key, value in stats[depute.ref].items())
            embed.add_field(
                name="Statistiques de vote",
                value=
                f"{stat_lines}"
            )
            embeds.append(embed)

        return embeds


    full_name = f"{first_name + ' ' if first_name else ''}{last_name}"
    return [error_handler(
        title="Député non trouvé",
        description=f"Je n'ai pas trouvé le député {full_name}."
    )]


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
    return error_handler(
        title="Scrutin non trouvé",
        description=f"Je n'ai pas trouvé le scrutin {code_ref}."
    )

