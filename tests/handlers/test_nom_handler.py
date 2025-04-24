from unittest.mock import patch, MagicMock, mock_open
import pytest
from discord import Embed

from config.config import DISCORD_EMBED_COLOR_MSG, DISCORD_EMBED_COLOR_ERR
from handlers.deputeHandler import nom_handler


def mock_depute():
    depute = MagicMock()
    depute.first_name = "Claire"
    depute.last_name = "Bernard"
    depute.url = "http://example.com/claire"
    depute.image = "http://example.com/claire.jpg"
    depute.to_string.return_value = "Claire Bernard, députée du Rhône"
    return depute



@pytest.mark.parametrize("name", ["Claire Bernard"])
@patch('os.listdir', return_value=["depute_data_rhone.json"])
@patch('utils.deputeManager.Depute.from_json_by_name', side_effect=lambda data, name: mock_depute() if name == "Claire Bernard" else None)
@patch('builtins.open', mock_open(read_data='{}'))
def test_nom_handler_found(_mock_from_json_by_name, _mock_listdir, name):
    embed = nom_handler(name)

    assert isinstance(embed, Embed)
    assert embed.title == "Claire Bernard"
    assert "Claire Bernard, députée du Rhône" in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_MSG



@pytest.mark.parametrize("name", ["Inconnu Nom", "Random Person"])
@patch('os.listdir', return_value=["depute_data_rhone.json", "depute_data_paris.json"])
@patch('utils.deputeManager.Depute.from_json_by_name', return_value=None)
@patch('builtins.open', mock_open(read_data='{}'))
def test_nom_handler_not_found(_mock_from_json_by_name, _mock_listdir, name):
    embed = nom_handler(name)

    assert embed.title == "Erreur"
    assert f"Je n'ai pas trouvé le député {name}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR



@pytest.mark.parametrize("name", ["Claire Bernard"])
@patch('os.listdir', return_value=[])
@patch('utils.deputeManager.Depute.from_json_by_name', return_value=None)
def test_nom_handler_no_files(_mock_listdir, _mock_from_json_by_name, name):
    embed = nom_handler(name)

    assert embed.title == "Erreur"
    assert f"Je n'ai pas trouvé le député {name}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR



@pytest.mark.parametrize("name", ["Claire Bernard"])
@patch('os.listdir', return_value=["depute_data_rhone.json"])
@patch('utils.deputeManager.Depute.from_json_by_name', side_effect=lambda data, name: mock_depute() if name == "Claire Bernard" else None)
@patch('builtins.open', mock_open(read_data='not json'))
def test_nom_handler_malformed_json(_mock_from_json_by_name, _mock_listdir, name):
    embed = nom_handler(name)

    assert embed.title == "Erreur"
    assert f"Je n'ai pas trouvé le député {name}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR
