import pytest
from discord import Embed
from handlers.deputeHandler import vote_handler
from tests.handlers.conftest import mock_folder_paths


@pytest.mark.parametrize("name, code_ref", [
    ("Panot", "3"),
])
def test_vote_handler_found(mock_folder_paths, name, code_ref):
    embed = vote_handler(name, code_ref)
    assert isinstance(embed, Embed)
    assert embed.title == "Mathilde Panot"
    assert embed.description
    assert int(embed.color) == 0x367588


@pytest.mark.parametrize("name, code_ref", [
    ("Fictitious", "3"),
    ("Panot", "9999"),
    ("Fictitious", "9999"),
])
def test_vote_handler_not_found(mock_folder_paths, name, code_ref):
    embed = vote_handler(name, code_ref)
    assert embed.title == "Erreur"
    assert f"Je n'ai pas trouvé le député {name} ou le scrutin {code_ref}." in embed.description
