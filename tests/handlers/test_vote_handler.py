from unittest.mock import patch, MagicMock, mock_open
import pytest
from discord import Embed

from common.config import DISCORD_EMBED_COLOR_MSG, DISCORD_EMBED_COLOR_ERR
from handlers.deputeHandler import vote_handler


def mock_depute():
    depute = MagicMock()
    depute.first_name = "Alice"
    depute.last_name = "Martin"
    depute.url = "http://example.com/depute"
    depute.image = "http://example.com/image.jpg"
    depute.to_string.return_value = "Alice Martin, députée de Lyon"
    return depute


def mock_scrutin():
    scrutin = MagicMock()
    scrutin.ref = "123"
    scrutin.sort = "adopté"
    scrutin.to_string_depute.return_value = "A voté POUR le texte."
    scrutin.dateScrutin = "2025-04-01"
    return scrutin



@pytest.mark.parametrize("name, code_ref", [("Martin", "123")])
@patch('os.listdir', return_value=["data.json"])
@patch('utils.scrutinManager.Scrutin.from_json_by_ref', return_value=mock_scrutin())
@patch('utils.deputeManager.Depute.from_json_by_name', return_value=mock_depute())
@patch('builtins.open', mock_open(read_data='{}'))
def test_vote_handler_success(_mock_depute, _mock_scrutin, _mock_listdir, name, code_ref):
    embeds = vote_handler(code_ref, name)

    assert isinstance(embeds, list)
    assert len(embeds) == 1
    embed = embeds[0]
    assert isinstance(embed, Embed)
    assert "Scrutin nº123" in embed.title
    assert ":calendar: **Date**: 2025-04-01" in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_MSG



@pytest.mark.parametrize("last_name, first_name,  code_ref", [("Martin", "Alice", "123")])
@patch('os.listdir', return_value=["data.json"])
@patch('utils.scrutinManager.Scrutin.from_json_by_ref', return_value=mock_scrutin())
@patch('utils.deputeManager.Depute.from_json_by_name', return_value=mock_depute())
@patch('builtins.open', mock_open(read_data='{}'))
def test_vote_handler_first_name_success(_mock_depute, _mock_scrutin, _mock_listdir, last_name, first_name, code_ref):
    embeds = vote_handler(code_ref, last_name, first_name)

    assert isinstance(embeds, list)
    assert len(embeds) == 1
    embed = embeds[0]
    assert isinstance(embed, Embed)
    assert "Scrutin nº123" in embed.title
    assert ":calendar: **Date**: 2025-04-01" in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_MSG


@pytest.mark.parametrize("name, code_ref", [("Martin", "999")])
@patch('os.listdir', return_value=["data.json"])
@patch('utils.scrutinManager.Scrutin.from_json_by_ref', return_value=None)
@patch('utils.deputeManager.Depute.from_json_by_name', return_value=mock_depute())
@patch('builtins.open', mock_open(read_data='{}'))
def test_vote_handler_scrutin_not_found(_mock_listdir, _mock_from_json_by_ref, _mock_from_json_by_name, name, code_ref):
    embed = vote_handler(code_ref, name)

    assert embed.title == "Scrutin non trouvé"
    assert f"Je n'ai pas trouvé le scrutin {code_ref}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR


@pytest.mark.parametrize("name, code_ref", [("Inconnu", "123")])
@patch('os.listdir', return_value=["data.json"])
@patch('utils.scrutinManager.Scrutin.from_json_by_ref', return_value=mock_scrutin())
@patch('utils.deputeManager.Depute.from_json_by_name', return_value=None)
@patch('builtins.open', mock_open(read_data='{}'))
def test_vote_handler_depute_not_found(_mock_listdir, _mock_from_json_by_ref, _mock_from_json_by_name, name, code_ref):
    embed = vote_handler(code_ref, name)

    assert embed.title == "Député non trouvé"
    assert f"Je n'ai pas trouvé le député {name}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR


@pytest.mark.parametrize("name, code_ref", [("Inconnu", "999")])
@patch('os.listdir', return_value=["data.json"])
@patch('utils.scrutinManager.Scrutin.from_json_by_ref', return_value=None)
@patch('utils.deputeManager.Depute.from_json_by_name', return_value=None)
@patch('builtins.open', mock_open(read_data='{}'))
def test_vote_handler_both_not_found(_mock_listdir, _mock_from_json_by_ref, _mock_from_json_by_name, name, code_ref):
    embed = vote_handler(code_ref, name)

    assert embed.title == "Député et scrutin non trouvé"
    assert f"Je n'ai trouvé ni le député {name}, ni le scrutin {code_ref}." == embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR


@pytest.mark.parametrize("name, code_ref", [("Martin", "123")])
@patch('os.listdir', return_value=["data.json"])
@patch('utils.scrutinManager.Scrutin.from_json_by_ref', side_effect=lambda data, code_ref: mock_scrutin())
@patch('utils.deputeManager.Depute.from_json_by_name', side_effect=lambda data, name: mock_depute())
@patch('builtins.open', mock_open(read_data='not json'))
def test_vote_handler_malformed_json(_mock_listdir, _mock_from_json_by_ref, _mock_from_json_by_name, name, code_ref):
    embed = vote_handler(code_ref, name)

    assert isinstance(embed, Embed)
    assert embed.title == "Député et scrutin non trouvé"
    assert f"Je n'ai trouvé ni le député {name}, ni le scrutin {code_ref}." == embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR