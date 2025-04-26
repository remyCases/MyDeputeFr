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
    depute.dep = "75"
    depute.dep_name = "Paris"
    depute.circo = "5"
    depute.gp = "LFI"
    return depute

def mock_depute_2():
    depute = MagicMock()
    depute.first_name = "Jean"
    depute.last_name = "Martin"
    depute.url = "http://example.com/jean"
    depute.image = "http://example.com/jean.jpg"
    depute.to_string.return_value = "Jean Martin, député du 75"
    depute.dep = "75"
    depute.dep_name = "Paris"
    depute.circo = "2"
    depute.gp = "Renaissance"
    return depute


@patch('os.listdir', return_value=["depute_data_75_01.json", "depute_data_99_10.json"])
@patch('utils.deputeManager.Depute.from_json_by_dep', side_effect=[mock_depute(), mock_depute_2()])
@patch('builtins.open', mock_open(read_data='{}'))
def test_dep_handler_found(_mock_depute, _mock_listdir):
    embed = dep_handler("75")
    print(embed.description)
    assert isinstance(embed, Embed)
    assert embed.title == f":pushpin: Département 75 (Paris)"
    assert (embed.description == "\n"
            .join([":bust_in_silhouette: [Jean Martin](http://example.com/jean) — :round_pushpin: **Circoncription** : 75-2 | :classical_building: **Groupe** : Renaissance",
                  ":bust_in_silhouette: [Lucie Durand](http://example.com/lucie) — :round_pushpin: **Circoncription** : 75-5 | :classical_building: **Groupe** : LFI"]))
    assert int(embed.color) == DISCORD_EMBED_COLOR_MSG


@pytest.mark.parametrize("code_dep", ["00", "XX"])
@patch('os.listdir', return_value=["depute_data_75_01.json", "depute_data_99_10.json"])
@patch('utils.deputeManager.Depute.from_json_by_dep', return_value=None)
@patch('builtins.open', mock_open(read_data='{}'))
def test_dep_handler_not_found(_mock_depute, _mock_listdir, code_dep):
    embed = dep_handler(code_dep)

    assert embed.title == "Député non trouvé"
    assert f"Je n'ai pas trouvé de députés dans le département {code_dep}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR


@pytest.mark.parametrize("code_dep", ["75"])
@patch('os.listdir', return_value=[])
@patch('utils.deputeManager.Depute.from_json_by_dep', return_value=None)
def test_dep_handler_no_files(_mock_listdir, _mock_depute, code_dep):
    embed = dep_handler(code_dep)

    assert embed.title == "Député non trouvé"
    assert f"Je n'ai pas trouvé de députés dans le département {code_dep}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR


@pytest.mark.parametrize("code_dep", ["75"])
@patch('os.listdir', return_value=["bad_file.json"])
@patch('utils.deputeManager.Depute.from_json_by_dep', side_effect=lambda data, code_dep: mock_depute() if "75" in data else None)
@patch('builtins.open', mock_open(read_data='not json'))
def test_dep_handler_malformed_json(_mock_depute, _mock_listdir, code_dep):
    embed = dep_handler(code_dep)

    assert isinstance(embed, Embed) or embed.title == "Député non trouvé"
    assert f"Je n'ai pas trouvé de députés dans le département {code_dep}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR