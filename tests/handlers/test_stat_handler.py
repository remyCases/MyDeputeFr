# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from discord import Embed

from handlers.deputeHandler import stat_handler
from tests.handlers.conftest import mock_folder_paths
from tests.handlers.conftest import valid_name, invalid_name


def test_found_depute(mock_folder_paths, valid_name):
    embed = stat_handler(valid_name[0])
    assert isinstance(embed, Embed)
    assert embed.title == valid_name[1]
    assert embed.description.startswith(valid_name[1])
    assert int(embed.color) == 0x367588

def test_not_found_depute(mock_folder_paths, invalid_name):
    embed = stat_handler(invalid_name)
    assert isinstance(embed, Embed)
    assert embed.title == "Erreur"
    assert embed.description == f"Je n'ai pas trouvé le député {invalid_name}."
    assert int(embed.color) == 0x367588

