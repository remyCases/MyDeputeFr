# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from __future__ import annotations

from typing import List, Optional

import discord

from config.config import ACTEUR_FOLDER, SCRUTINS_FOLDER, DISCORD_EMBED_COLOR_DEBUG
from handlers.commonHandler import error_handler
from utils.deputeManager import Depute
from utils.scrutinManager import Scrutin
from utils.utils import read_files_from_directory


def debugd_handler(last_name: str, first_name: Optional[str] = None) -> List[discord.Embed]:
    """
    Return an embed with debug info of a député by name.

    Parameters:
        last_name (str): The last_name of the député to search.
        first_name (str | None): The optional first name of the député.
    """
    deputes = [ depute for data in read_files_from_directory(ACTEUR_FOLDER)
                if (depute := Depute.from_json_by_name(data, last_name, first_name)) ]
    if len(deputes) > 0 :
        deputes.sort(key=lambda x: int(x.circo))
        return [
            discord.Embed(
                title=f"{depute.first_name} {depute.last_name}",
                description=depute,
                color=DISCORD_EMBED_COLOR_DEBUG,
            )
            for depute in deputes
        ]
    full_name = f"{first_name + ' ' if first_name else ''}{last_name}"
    return [ error_handler(
        title="Député non trouvé",
        description=f"Je n'ai pas trouvé le député {full_name}."
    ) ]


def debugs_handler(code_ref: str) -> discord.Embed:
    """
    Return an embed with debug info of a scrutin by code reference.

    Parameters:
        code_ref (str): The reference code of the scrutin.
    """
    for data in read_files_from_directory(SCRUTINS_FOLDER):
        if scrutin := Scrutin.from_json_by_ref(data, code_ref):
            embed = discord.Embed(
                title=f"Scrutin nº{scrutin.ref}",
                description=scrutin,
                color=DISCORD_EMBED_COLOR_DEBUG,
            )
            return embed

    return error_handler(description=f"Je n'ai pas trouvé le scrutin {code_ref}.")

def debugn_handler(ref_notifs: List[str]) -> List[discord.Embed]:
    """
    Return an embed with debug info of a scrutin by code reference.

    Parameters:
        code_ref (str): The reference code of the scrutin.
    """
    embeds: List[discord.Embed] = []
    for depute_id in ref_notifs:
        for data in read_files_from_directory(ACTEUR_FOLDER):
            if depute := Depute.from_json_by_ref(data, depute_id):
                embeds.append(discord.Embed(
                    title=depute_id,
                    description=depute,
                    color=DISCORD_EMBED_COLOR_DEBUG,
                ))
    return embeds
