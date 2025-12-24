from unittest.mock import patch, MagicMock, mock_open

import pytest
from discord import Embed

from common.config import DISCORD_EMBED_COLOR_MSG, DISCORD_EMBED_COLOR_ERR
from handlers.deputeHandler import nom_handler

def mock_depute(last_name: str, first_name: str, circo: str) -> MagicMock:
    depute = MagicMock()
    depute.first_name = first_name
    depute.last_name = last_name
    depute.url = f"http://example.com/{last_name.replace(' ', '_').lower()}"
    depute.image = f"http://example.com/{last_name.replace(' ', '_').lower()}.jpg"
    depute.dep = "69"
    depute.circo = circo
    depute.dep_name = "Rhône"
    depute.gp = "Groupe"
    return depute



@patch('os.listdir', return_value=["depute_1.json"])
@patch('utils.deputeManager.Depute.from_json_by_name',
       side_effect=[mock_depute("Bernard", "Claire", "1")])
@patch('builtins.open', mock_open(read_data='{}'))
def test_nom_handler_found(
    _mock_from_json_by_name: MagicMock,
    _mock_listdir: MagicMock) -> None:
    embeds = nom_handler("Bernard")

    assert isinstance(embeds, list)
    assert len(embeds) == 1
    embed = embeds[0]
    assert isinstance(embed, Embed)
    assert embed.title == ":bust_in_silhouette: Claire Bernard"
    assert ":round_pushpin: **Circoncription** : 69-1 (Rhône)\n:classical_building: **Groupe** : Groupe" == embed.description
    assert embed.colour is not None
    assert int(embed.colour) == DISCORD_EMBED_COLOR_MSG


@patch('os.listdir', return_value=["depute_1.json", "depute_2.json", "depute_3.json", "depute_4.json"])
@patch('utils.deputeManager.Depute.from_json_by_name',
       side_effect=[
           mock_depute("Bernard", "Sam", "2"),
           mock_depute("Bernard", "Claire", "1"),
           None,
           mock_depute("Bernard", "Bob", "3")
       ])
@patch('builtins.open', mock_open(read_data='{}'))
def test_nom_handler_found_multiple(
    _mock_from_json_by_name: MagicMock, 
    _mock_listdir: MagicMock) -> None:
    embeds = nom_handler("Bernard")

    assert isinstance(embeds, list)
    assert len(embeds) == 3
    assert embeds[0].title == ":bust_in_silhouette: Bob Bernard"
    assert embeds[1].title == ":bust_in_silhouette: Claire Bernard"
    assert embeds[2].title == ":bust_in_silhouette: Sam Bernard"

@patch('os.listdir', return_value=["depute_1.json", "depute_2.json", "depute_3.json", "depute_4.json"])
@patch('utils.deputeManager.Depute.from_json_by_name',
       side_effect=[
           mock_depute("Bernard", "Sam", "2"),
           None,
           None,
           None
       ])
@patch('builtins.open', mock_open(read_data='{}'))
def test_nom_handler_found_first_name(
    _mock_from_json_by_name: MagicMock, 
    _mock_listdir: MagicMock) -> None:
    embeds = nom_handler("Bernard", "Sam")

    assert isinstance(embeds, list)
    assert len(embeds) == 1
    assert embeds[0].title == ":bust_in_silhouette: Sam Bernard"

@pytest.mark.parametrize("name", ["Inconnu"])
@patch('os.listdir', return_value=["depute_1.json", "depute_2.json"])
@patch('utils.deputeManager.Depute.from_json_by_name', return_value=[])
@patch('builtins.open', mock_open(read_data='{}'))
def test_nom_handler_not_found(
    _mock_from_json_by_name: MagicMock, 
    _mock_listdir: MagicMock, 
    name: str) -> None:
    embed = nom_handler(name)

    assert isinstance(embed, Embed) 
    assert embed.title == "Député non trouvé"
    assert embed.description is not None
    assert f"Je n'ai pas trouvé le député {name}." in embed.description
    assert embed.colour is not None
    assert int(embed.colour) == DISCORD_EMBED_COLOR_ERR


@pytest.mark.parametrize("name", ["Bernard"])
@patch('os.listdir', return_value=[])
@patch('utils.deputeManager.Depute.from_json_by_name', return_value=[])
def test_nom_handler_no_files(
    _mock_listdir: MagicMock, 
    _mock_from_json_by_name: MagicMock, 
    name: str) -> None:
    embed = nom_handler(name)

    assert isinstance(embed, Embed) 
    assert embed.title == "Député non trouvé"
    assert embed.description is not None
    assert f"Je n'ai pas trouvé le député {name}." in embed.description
    assert embed.colour is not None
    assert int(embed.colour) == DISCORD_EMBED_COLOR_ERR


@pytest.mark.parametrize("name", ["Bernard"])
@patch('os.listdir', return_value=["depute_1.json"])
@patch('utils.deputeManager.Depute.from_json_by_name',
       side_effect=[mock_depute("Bernard", "Claire", "1")])
@patch('builtins.open', mock_open(read_data='not json'))
def test_nom_handler_malformed_json(
    _mock_from_json_by_name: MagicMock, 
    _mock_listdir: MagicMock, 
    name: str) -> None:
    embed = nom_handler(name)

    assert isinstance(embed, Embed) 
    assert embed.title == "Député non trouvé"
    assert embed.description is not None
    assert f"Je n'ai pas trouvé le député {name}." in embed.description
    assert embed.colour is not None
    assert int(embed.colour) == DISCORD_EMBED_COLOR_ERR
