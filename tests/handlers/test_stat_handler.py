from unittest.mock import patch, MagicMock, mock_open
import pytest
from discord import Embed

from config.config import DISCORD_EMBED_COLOR_MSG, DISCORD_EMBED_COLOR_ERR
from handlers.deputeHandler import stat_handler
from utils.scrutinManager import ResultBallot


def mock_depute():
    depute = MagicMock()
    depute.first_name = "Nora"
    depute.last_name = "Lemoine"
    depute.url = "http://example.com/nora"
    depute.image = "http://example.com/nora.jpg"
    depute.to_string.return_value = "Nora Lemoine, députée de l'Hérault"
    return depute


def make_mock_scrutin(result: ResultBallot):
    scrutin = MagicMock()
    scrutin.result.return_value = result
    scrutin.to_string_depute.return_value = f"Vote: {result.name}"
    return scrutin



@pytest.mark.parametrize("name", [("Nora Lemoine")])
@patch('os.listdir', side_effect=[["depute_herault.json"], ["scrutin1.json", "scrutin2.json", "scrutin3.json"]])
@patch('utils.scrutinManager.Scrutin.from_json', side_effect=[
    make_mock_scrutin(ResultBallot.POUR),
    make_mock_scrutin(ResultBallot.CONTRE),
    make_mock_scrutin(ResultBallot.ABSTENTION)
])
@patch('utils.deputeManager.Depute.from_json_by_name', side_effect=lambda data, name: mock_depute() if name == "Nora Lemoine" else None)
@patch('builtins.open', mock_open(read_data='{}'))
def test_stat_handler_valid(_mock_depute, _mock_scrutin_from_json, _mock_listdir, name):
    embed = stat_handler(name)

    assert isinstance(embed, Embed)
    assert embed.title == "Nora Lemoine"
    assert "pour': 1" in embed.description
    assert "contre': 1" in embed.description
    assert "abstention': 1" in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_MSG



@pytest.mark.parametrize("name", [("Jean Perdu")])
@patch('os.listdir', return_value=["depute_data.json"])
@patch('utils.deputeManager.Depute.from_json_by_name', return_value=None)
@patch('builtins.open', mock_open(read_data='{}'))
def test_stat_handler_not_found(_mock_depute, _mock_listdir, name):
    embed = stat_handler(name)

    assert embed.title == "Erreur"
    assert f"Je n'ai pas trouvé le député {name}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR



@pytest.mark.parametrize("name", [("Nora Lemoine")])
@patch('os.listdir', side_effect=[[], []])
@patch('utils.deputeManager.Depute.from_json_by_name', return_value=None)
def test_stat_handler_no_files(_mock_listdir, _mock_depute, name):
    embed = stat_handler(name)

    assert embed.title == "Erreur"
    assert f"Je n'ai pas trouvé le député {name}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR


@pytest.mark.parametrize("name", [("Nora Lemoine")])
@patch('os.listdir', side_effect=[["depute_data.json"], ["scrutin1.json"]])
@patch('utils.scrutinManager.Scrutin.from_json', side_effect=[make_mock_scrutin(ResultBallot.NONVOTANT)])
@patch('utils.deputeManager.Depute.from_json_by_name', side_effect=lambda data, name: mock_depute())
@patch('builtins.open', mock_open(read_data='not json'))
def test_stat_handler_malformed_json(_mock_depute, _mock_scrutin, _mock_listdir, name):
    embed = stat_handler(name)

    assert embed.title == "Erreur"
    assert f"Je n'ai pas trouvé le député {name}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR

