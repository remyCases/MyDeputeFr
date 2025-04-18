# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import discord

from config.config import ACTEUR_FOLDER, SCRUTINS_FOLDER, DISCORD_EMBED_COLOR_DEBUG
from handlers.commonHandler import error_handler
from utils.deputeManager import Depute
from utils.scrutinManager import Scrutin
from utils.utils import read_files_from_directory


def debugd_handler(name: str) -> discord.Embed:
    """
    Return an embed with debug info of a député by name.

    Parameters:
        name (str): The name of the député to search.
    """
    for data in read_files_from_directory(ACTEUR_FOLDER):
        if depute := Depute.from_json_by_name(data, name):
            embed = discord.Embed(
                title=f"{depute.first_name} {depute.last_name}",
                description=depute,
                color=DISCORD_EMBED_COLOR_DEBUG,
            )
            return embed

    return error_handler(description=f"Je n'ai pas trouvé le député {name}.")


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