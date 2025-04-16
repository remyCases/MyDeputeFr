import pytest
from discord import Embed
from handlers.deputeHandler import ciro_handler
from tests.handlers.conftest import mock_folder_paths


@pytest.mark.parametrize("code_dep, code_circo", [
    ("93", "10"),
])
def test_ciro_handler_found(mock_folder_paths, code_dep, code_circo):
    embed = ciro_handler(code_dep, code_circo)
    assert isinstance(embed, Embed)
    assert embed.title
    assert embed.description
    assert int(embed.color) == 0x367588


@pytest.mark.parametrize("code_dep, code_circo", [
    ("00", "00"),
    ("AB", "CD"),
])
def test_ciro_handler_not_found(mock_folder_paths, code_dep, code_circo):
    embed = ciro_handler(code_dep, code_circo)
    assert embed.title == "Erreur"
    assert f"J'ai pas trouvé de député dans le {code_dep}-{code_circo}." in embed.description
