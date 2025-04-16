# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import pytest
from discord import Embed

from handlers.deputeHandler import scr_handler
from tests.handlers.conftest import mock_folder_paths


def test_found_scrutin(mock_folder_paths):
    code_ref = "3"
    embed = scr_handler(code_ref)
    assert isinstance(embed, Embed)
    assert embed.title == ":green_circle:  Scrutin nº3"
    assert "2024-10-09" in embed.description
    assert "adopté" in embed.description
    assert int(embed.color) == 0x367588


@pytest.fixture(params=["99999999999999999999999999999999999999999", "-1", "code_ref"])
def invalid_code_ref(request):
    return request.param

def test_not_found_scrutin(mock_folder_paths, invalid_code_ref):
    from handlers.deputeHandler import scr_handler
    embed = scr_handler(invalid_code_ref)
    assert embed.title == "Erreur"
    assert embed.description == f"Je n'ai pas trouvé le scrutin {invalid_code_ref}."
    assert int(embed.color) == 0x367588
