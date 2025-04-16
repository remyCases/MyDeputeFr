import pytest
from discord import Embed
from handlers.deputeHandler import dep_handler
from tests.handlers.conftest import mock_folder_paths


@pytest.mark.parametrize("code_dep", ["93"])
def test_dep_handler_found(mock_folder_paths, code_dep):
    embed = dep_handler(code_dep)
    assert isinstance(embed, Embed)
    assert embed.title == "Députés"
    assert embed.description
    assert int(embed.color) == 0x367588


@pytest.mark.parametrize("code_dep", ["00", "AB"])
def test_dep_handler_not_found(mock_folder_paths, code_dep):
    embed = dep_handler(code_dep)
    assert embed.title == "Erreur"
    assert f"J'ai pas trouvé de députés dans le département {code_dep}." in embed.description
