# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import pytest

from discord import Embed

from handlers.deputeHandler import stat_handler
from tests.handlers.conftest import mock_folder_paths


@pytest.fixture(params=[
    ("Panot", "Mathilde Panot"),
    ("PaNoT", "Mathilde Panot"),
    ("Le Pen", "Marine Le Pen"),
    ("LePen", "Marine Le Pen"),
    ("Trébuchet", "Vincent Trébuchet"),
    ("Trebuchet", "Vincent Trébuchet"),
    ("Thiébault-Martinez", "Céline Thiébault-Martinez"),
    ("Thiébault Martinez", "Céline Thiébault-Martinez"),
    ("Thiebault Martinez", "Céline Thiébault-Martinez"),
    ("ThiebaultMartinez", "Céline Thiébault-Martinez"),
    ("D'Intorni", "Christelle D'Intorni"),
    ("D Intorni", "Christelle D'Intorni"),
    ("DIntorni", "Christelle D'Intorni")
])
def valid_name(request):
    return request.param


@pytest.fixture(params=["Jane Doe", "John Smith", "Unknown"])
def invalid_name(request):
    return request.param

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

