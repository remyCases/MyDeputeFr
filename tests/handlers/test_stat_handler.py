from unittest.mock import patch, MagicMock, mock_open
import pytest
from discord import Embed

from common.config import DISCORD_EMBED_COLOR_MSG, DISCORD_EMBED_COLOR_ERR
from handlers.deputeHandler import stat_handler
from utils.scrutinManager import ResultBallot


def mock_depute(first_name="Nora", last_name="Lemoine", circo="1"):
    depute = MagicMock()
    depute.first_name = first_name
    depute.last_name = last_name
    depute.url = f"http://example.com/{last_name.lower()}"
    depute.image = f"http://example.com/{last_name.lower()}.jpg"
    depute.dep = "34"
    depute.dep_name = "Hérault"
    depute.circo = circo
    depute.gp = "Groupe"
    depute.ref = "nora-lemoine"
    return depute


def make_mock_scrutin(result: ResultBallot):
    scrutin = MagicMock()
    scrutin.result.return_value = result
    scrutin.to_string_depute.return_value = f"Vote: {result.name}"
    return scrutin


@patch('os.listdir', return_value=["depute.json"])
@patch('utils.scrutinManager.Scrutin.from_json', side_effect=[
    make_mock_scrutin(ResultBallot.POUR),
    make_mock_scrutin(ResultBallot.CONTRE),
    make_mock_scrutin(ResultBallot.ABSTENTION)
])
@patch('utils.deputeManager.Depute.from_json_by_name',
       side_effect=[mock_depute()])
@patch('builtins.open', mock_open(read_data='{}'))
def test_stat_handler_found(_mock_from_json_by_name, _mock_scrutin, _mock_listdir):
    embeds = stat_handler("Lemoine", "Nora")

    assert isinstance(embeds, list)
    assert len(embeds) == 1
    embed = embeds[0]
    assert isinstance(embed, Embed)
    assert embed.title == ":bust_in_silhouette: Nora Lemoine"
    assert embed.fields[0].name == "Statistiques de vote"
    assert ":green_circle: Pour" in embed.fields[0].value
    assert ":red_circle: Contre" in embed.fields[0].value
    assert ":white_circle: Abstention" in embed.fields[0].value
    assert int(embed.color) == DISCORD_EMBED_COLOR_MSG


@pytest.mark.parametrize("last_name", ["Perdu"])
@patch('os.listdir', return_value=["depute.json"])
@patch('utils.deputeManager.Depute.from_json_by_name', return_value=None)
@patch('builtins.open', mock_open(read_data='{}'))
def test_stat_handler_depute_not_found(_mock_from_json_by_name, _mock_listdir, last_name):
    embed = stat_handler(last_name)

    assert embed.title == "Député non trouvé"
    assert f"Je n'ai pas trouvé le député {last_name}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR


@pytest.mark.parametrize("last_name", ["Lemoine"])
@patch('os.listdir', return_value=[])
@patch('utils.deputeManager.Depute.from_json_by_name', return_value=None)
def test_stat_handler_no_files(_mock_from_json_by_name, _mock_listdir, last_name):
    embed = stat_handler(last_name)

    assert embed.title == "Député non trouvé"
    assert f"Je n'ai pas trouvé le député {last_name}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR


@pytest.mark.parametrize("last_name", ["Lemoine"])
@patch('os.listdir', side_effect=[["depute_data.json"], ["scrutin1.json"]])
@patch('utils.scrutinManager.Scrutin.from_json', side_effect=[make_mock_scrutin(ResultBallot.NONVOTANT)])
@patch('utils.deputeManager.Depute.from_json_by_name', side_effect=[mock_depute()])
@patch('builtins.open', mock_open(read_data='not json'))
def test_stat_handler_malformed_json(_mock_from_json_by_name, _mock_scrutin, _mock_listdir, last_name):
    embed = stat_handler(last_name)

    assert embed.title == "Député non trouvé"
    assert f"Je n'ai pas trouvé le député {last_name}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR
