# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.
from __future__ import annotations

from typing import Optional

import discord

from common.config import SCRUTINS_FOLDER, ACTEUR_FOLDER, DISCORD_EMBED_COLOR_MSG
from common.strings import DEPUTE_EMBED_DESCRIPTION, DEPUTE_EMBED_TITLE, SCRUTIN_EMBED_TITLE, SCRUTIN_EMBED_DESCRIPTION, \
    VOTE_EMOJI_POUR, VOTE_EMOJI_CONTRE, VOTE_EMOJI_ABSTENTION, VOTE_EMOJI_NON_VOTANT, \
    DEPUTE_NOT_FOUND_TITLE, DEPARTEMENT_DEPUTE_DESCRIPTION, DEPARTEMENT_TITLE, CIRCO_DEPUTE_NOT_FOUND_DESCRIPTION, \
    DEPARTEMENT_DEPUTE_NOT_FOUND_DESCRIPTION, SCRUTIN_NOT_FOUND_TITLE, DEPUTE_NOT_FOUND_DESCRIPTION, \
    SCRUTIN_NOT_FOUND_DESCRIPTION, SCRUTIN_DEPUTE_NOT_FOUND_DESCRIPTION, SCRUTIN_DEPUTE_NOT_FOUND_TITLE, \
    SCRUTIN_PARTICIPATION_NAME, SCRUTIN_RESULTS_NAME, SCRUTIN_RESULTS_VALUE, SCRUTIN_PARTICIPATION_VALUE, \
    STATISTICS_FIELD_NAME, VOTE_TITLE, VOTE_DESCRIPTION, VOTE_EMOJI_ABSENT, VOTE_VALUE_POUR, VOTE_VALUE_CONTRE, \
    VOTE_VALUE_ABSTENTION, VOTE_VALUE_NON_VOTANT, VOTE_VALUE_ABSENT, SCRUTIN_EMOJI_ADOPTE, SCRUTIN_EMOJI_REJETE, \
    SCRUTIN_VALUE_ADOPTE
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
        title=DEPUTE_EMBED_TITLE.format(
            first_name=depute.first_name,
            last_name=depute.last_name
        ),
        description=DEPUTE_EMBED_DESCRIPTION.format(
            dep=depute.dep,
            circo=depute.circo,
            dep_name=depute.dep_name,
            gp=depute.gp
        ),
        color=DISCORD_EMBED_COLOR_MSG,
        url=depute.url
    ).set_thumbnail(url=depute.image)


def __scrutin_to_embed(scrutin: Scrutin):
    embed = discord.Embed(
        title=SCRUTIN_EMBED_TITLE.format(ref=scrutin.ref),
        description=SCRUTIN_EMBED_DESCRIPTION.format(
            date_scrutin=scrutin.dateScrutin,
            text=scrutin.titre,
            result=f"{SCRUTIN_EMOJI_ADOPTE} {SCRUTIN_EMOJI_ADOPTE}"
            if scrutin.sort == 'adopté'
            else f"{SCRUTIN_VALUE_ADOPTE} {SCRUTIN_EMOJI_REJETE}"
        ),
        color=DISCORD_EMBED_COLOR_MSG,
    )
    return embed


def __vote_emoticon(k: str) -> str:
    """
    Returns an emoji corresponding to a given key.

    Parameters:
        k (str): The key representing the type of vote.
            Valid keys include (case insentive):
                - "pour"
                - "contre"
                - "abstention"
                - "nonvotant"
                - "absent"
    Returns:
        str: The corresponding emoji as a string, or an empty string if the key is not recognized.
    """
    k = k.lower()
    return {
        "pour": VOTE_EMOJI_POUR,
        "contre": VOTE_EMOJI_CONTRE,
        "abstention": VOTE_EMOJI_ABSTENTION,
        "nonvotant": VOTE_EMOJI_NON_VOTANT,
        "absent": VOTE_EMOJI_ABSENT,
    }.get(k, "")


def __vote_value(k: str) -> str:
    """
    Returns an vote value corresponding to a given key.

    Parameters:
        k (str): The key representing the type of vote.
            Valid keys include (case insentive):
                - "pour"
                - "contre"
                - "abstention"
                - "nonvotant"
                - "absent"
    Returns:
        str: The corresponding value as a string, or an empty string if the key is not recognized.
    """
    k = k.lower()
    return {
        "pour": VOTE_VALUE_POUR,
        "contre": VOTE_VALUE_CONTRE,
        "abstention": VOTE_VALUE_ABSTENTION,
        "nonvotant": VOTE_VALUE_NON_VOTANT,
        "absent": VOTE_VALUE_ABSENT,
    }.get(k, "")


def nom_handler(last_name: str, first_name: Optional[str] = None) -> list[discord.Embed] | discord.Embed:
    """
    Retrieve embeds with député information based on the given name.

    Parameters:
        last_name (str): The last name of the député.
        first_name (Optional[str]): The optional first name of the député.

    Returns:
        list[discord.Embed]: A list of embeds with député info or an error message.
    """
    deputes = [ depute for data in read_files_from_directory(ACTEUR_FOLDER)
                if (depute := Depute.from_json_by_name(data, last_name, first_name)) ]
    if len(deputes) > 0 :
        deputes.sort(key=lambda x: x.first_name)
        return [
            __depute_to_embed(depute)
            for depute in deputes
        ]
    full_name = f"{first_name + ' ' if first_name else ''}{last_name}"
    return error_handler(
        title=DEPUTE_NOT_FOUND_TITLE,
        description=DEPUTE_NOT_FOUND_DESCRIPTION.format(full_name=full_name)
    )


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
        title=DEPUTE_NOT_FOUND_TITLE,
        description=CIRCO_DEPUTE_NOT_FOUND_DESCRIPTION.format(code_dep=code_dep, code_circo=code_circo)
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
            DEPARTEMENT_DEPUTE_DESCRIPTION.format(
                first_name=depute.first_name,
                last_name=depute.last_name,
                url=depute.url,
                dep=depute.dep,
                circo=depute.circo,
                dep_name=depute.dep_name,
                gp=depute.gp
            )
            for depute in deputes
        ])
        return discord.Embed(
            title=DEPARTEMENT_TITLE.format(
                dep=deputes[0].dep,
                dep_name=deputes[0].dep_name
            ),
            description=description,
            color=DISCORD_EMBED_COLOR_MSG,
        )

    return error_handler(title=DEPUTE_NOT_FOUND_TITLE, description=DEPARTEMENT_DEPUTE_NOT_FOUND_DESCRIPTION.format(code_dep=code_dep))


def vote_handler(code_ref: str, last_name: str, first_name: Optional[str] = None) -> list[discord.Embed] | discord.Embed:
    """
    Return embed showing how a député voted in a scrutin.

    Parameters:
        code_ref (str): Reference of the scrutin.
        last_name (str): The last name of the député.
        first_name (Optional[str]): The optional first name of the député.

    Returns:
        discord.Embed: Embed showing the voting result or error.
    """
    deputes = [
        depute for x in read_files_from_directory(ACTEUR_FOLDER) if (depute := Depute.from_json_by_name(x, last_name, first_name))
    ]
    scrutin : Scrutin | None = next(
        (scrutin for x in read_files_from_directory(SCRUTINS_FOLDER) if (scrutin := Scrutin.from_json_by_ref(x, code_ref))),
        None
    )
    if scrutin and len(deputes) > 0:
        deputes.sort(key=lambda x: x.first_name)
        embeds = []
        for depute in deputes:
            embed = __scrutin_to_embed(scrutin)
            embed.title += f" - {depute.first_name} {depute.last_name}"
            position = scrutin.depute_vote(depute)
            vote = VOTE_DESCRIPTION.format(
                depute_first_name = depute.first_name,
                depute_last_name=depute.last_name,
                depute_dep=depute.dep,
                depute_dep_name=depute.dep_name,
                depute_circo=depute.circo,
                depute_gp=depute.gp,
                position_name=__vote_value(scrutin.depute_vote(depute).name),
                position_name_emoji=__vote_emoticon(position.name),
            )
            embed.add_field(
                name=VOTE_TITLE,
                value=vote,
            )
            embed.set_thumbnail(url=depute.image)
            embeds.append(embed)
        return embeds
    elif scrutin:
        full_name = f"{first_name + ' ' if first_name else ''}{last_name}"
        return error_handler(
            title=DEPUTE_NOT_FOUND_TITLE,
            description=DEPUTE_NOT_FOUND_DESCRIPTION.format(full_name=full_name)
        )
    elif len(deputes) > 0:
        return error_handler(
            title=SCRUTIN_NOT_FOUND_TITLE,
            description=SCRUTIN_NOT_FOUND_DESCRIPTION.format(code_ref=code_ref)
        )
    else:
        full_name = f"{first_name + ' ' if first_name else ''}{last_name}"
        return error_handler(
            title=SCRUTIN_DEPUTE_NOT_FOUND_TITLE,
            description=SCRUTIN_DEPUTE_NOT_FOUND_DESCRIPTION.format(code_ref=code_ref, full_name=full_name)
        )




def stat_handler(last_name: str, first_name: Optional[str] = None) -> list[discord.Embed] | discord.Embed:
    """
    Return embed with voting statistics for a député.

    Parameters:
        last_name (str): The last name of the député.
        first_name (Optional[str]): The optional first name of the député.

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
            stat_lines = "\n".join(f"{__vote_emoticon(key)} {__vote_value(key)} : {value}" for key, value in stats[depute.ref].items())
            embed.add_field(
                name=STATISTICS_FIELD_NAME,
                value=
                f"{stat_lines}"
            )
            embeds.append(embed)

        return embeds


    full_name = f"{first_name + ' ' if first_name else ''}{last_name}"
    return error_handler(
        title=DEPUTE_NOT_FOUND_TITLE,
        description=DEPUTE_NOT_FOUND_DESCRIPTION.format(full_name=full_name)
    )


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
            embed = __scrutin_to_embed(scrutin)
            embed.add_field(
                name=SCRUTIN_PARTICIPATION_NAME,
                value=SCRUTIN_PARTICIPATION_VALUE.format(
                    nombreVotants=scrutin.nombreVotants,
                    nonVotant=scrutin.nonVotant,
                    nonVotantsVolontaire=scrutin.nonVotantsVolontaire
                ),
                inline=True
            )
            embed.add_field(
                name=SCRUTIN_RESULTS_NAME,
                value=SCRUTIN_RESULTS_VALUE.format(
                    pour=scrutin.pour,
                    contre=scrutin.contre,
                    abstention=scrutin.abstention
                ),
                inline=True
            )
            return embed
    return error_handler(
        title=SCRUTIN_NOT_FOUND_TITLE,
        description=SCRUTIN_NOT_FOUND_DESCRIPTION.format(code_ref=code_ref)
    )

