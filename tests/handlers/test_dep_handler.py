from unittest.mock import patch, MagicMock, mock_open
import pytest
from discord import Embed

from config.config import DISCORD_EMBED_COLOR_MSG, DISCORD_EMBED_COLOR_ERR
from handlers.deputeHandler import dep_handler


def mock_depute():
    depute = MagicMock()
    depute.first_name = "Lucie"
    depute.last_name = "Durand"
    depute.url = "http://example.com/lucie"
    depute.image = "http://example.com/lucie.jpg"
    depute.to_string.return_value = "Lucie Durand, députée du 75"
    return depute


@pytest.mark.parametrize("code_dep", ["75"])
@patch('os.listdir', return_value=["depute_data_75_01.json", "depute_data_99_10.json"])
@patch('utils.deputeManager.Depute.from_json_by_dep', return_value=mock_depute())
@patch('builtins.open', mock_open(read_data='{}'))
def test_dep_handler_found(_mock_depute, _mock_listdir, code_dep):
    embed = dep_handler(code_dep)

    assert isinstance(embed, Embed)
    assert embed.title == f"Département {code_dep}"
    assert "Lucie Durand, députée du 75" in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_MSG


@pytest.mark.parametrize("code_dep", ["00", "XX"])
@patch('os.listdir', return_value=["depute_data_75_01.json", "depute_data_99_10.json"])
@patch('utils.deputeManager.Depute.from_json_by_dep', return_value=None)
@patch('builtins.open', mock_open(read_data='{}'))
def test_dep_handler_not_found(_mock_depute, _mock_listdir, code_dep):
    embed = dep_handler(code_dep)

    assert embed.title == "Erreur"
    assert f"Je n'ai pas trouvé de députés dans le département {code_dep}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR


@pytest.mark.parametrize("code_dep", ["75"])
@patch('os.listdir', return_value=[])
@patch('utils.deputeManager.Depute.from_json_by_dep', return_value=None)
def test_dep_handler_no_files(_mock_listdir, _mock_depute, code_dep):
    embed = dep_handler(code_dep)

    assert embed.title == "Erreur"
    assert f"Je n'ai pas trouvé de députés dans le département {code_dep}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR


@pytest.mark.parametrize("code_dep", ["75"])
@patch('os.listdir', return_value=["bad_file.json"])
@patch('utils.deputeManager.Depute.from_json_by_dep', side_effect=lambda data, code_dep: mock_depute() if "75" in data else None)
@patch('builtins.open', mock_open(read_data='not json'))
def test_dep_handler_malformed_json(_mock_depute, _mock_listdir, code_dep):
    embed = dep_handler(code_dep)

    assert isinstance(embed, Embed) or embed.title == "Erreur"
    assert f"Je n'ai pas trouvé de députés dans le département {code_dep}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR