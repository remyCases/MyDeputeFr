import pytest
from discord import Embed
from handlers.deputeHandler import nom_handler
from tests.handlers.conftest import mock_folder_paths


@pytest.fixture(params=[
    ("Panot", "Mathilde Panot"),
    ("Thiebault Martinez", "Céline Thiébault-Martinez"),
])
def valid_name(request):
    return request.param


@pytest.fixture(params=["Unknown", "Fictitious Name"])
def invalid_name(request):
    return request.param


def test_nom_handler_found(mock_folder_paths, valid_name):
    embed = nom_handler(valid_name[0])
    assert isinstance(embed, Embed)
    assert embed.title == valid_name[1]
    assert embed.url
    assert embed.thumbnail.url
    assert int(embed.color) == 0x367588


def test_nom_handler_not_found(mock_folder_paths, invalid_name):
    embed = nom_handler(invalid_name)
    assert embed.title == "Erreur"
    assert f"J'ai pas trouvé le député {invalid_name}." in embed.description
