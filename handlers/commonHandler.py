# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from config.config import DISCORD_EMBED_COLOR_ERR
import discord

def error_handler(title: str = "Erreur", description: str = "Une erreur inconnue est survenu") -> discord.Embed:
    """
    Return a generic error embed message.

    Parameters:
        title (str): Embed title.
        description (str): Error description.

    Returns:
        discord.Embed: The error message embed.
    """
    return discord.Embed(
        title=title,
        description=description,
        color=DISCORD_EMBED_COLOR_ERR,
    )
