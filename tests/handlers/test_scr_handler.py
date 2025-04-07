from unittest.mock import patch, MagicMock, mock_open
import pytest
from discord import Embed

from config.config import DISCORD_EMBED_COLOR_MSG, DISCORD_EMBED_COLOR_ERR
from handlers.deputeHandler import scr_handler


def mock_scrutin_adopte():
    scrutin = MagicMock()
    scrutin.ref = "456"
    scrutin.sort = "adopté"
    scrutin.titre = "Projet de loi sur l'énergie propre."
    scrutin.dateScrutin = "2025-04-01"
    scrutin.nombreVotants = 577
    scrutin.nonVotant = 10
    scrutin.nonVotantsVolontaire = 5
    scrutin.pour = 300
    scrutin.contre = 200
    scrutin.abstention = 67
    return scrutin


@pytest.mark.parametrize("code_ref", [("456")])
@patch('os.listdir', return_value=["scrutin_456.json"])
@patch('utils.scrutinManager.Scrutin.from_json_by_ref', side_effect=lambda data, ref: mock_scrutin_adopte() if ref == "456" else None)
@patch('builtins.open', mock_open(read_data='{}'))
def test_scr_handler_found(_mock_scrutin, _mock_listdir, code_ref):
    embed = scr_handler(code_ref)

    assert isinstance(embed, Embed)
    assert f"Scrutin nº{code_ref}" in embed.title
    assert "Projet de loi sur l'énergie propre" in embed.description
    assert ":green_circle:" in embed.title
    assert int(embed.color) == DISCORD_EMBED_COLOR_MSG


@pytest.mark.parametrize("code_ref", [("999"), ("ABC")])
@patch('os.listdir', return_value=["scrutin_456.json"])
@patch('utils.scrutinManager.Scrutin.from_json_by_ref', return_value=None)
@patch('builtins.open', mock_open(read_data='{}'))
def test_scr_handler_not_found(_mock_scrutin, _mock_listdir, code_ref):
    embed = scr_handler(code_ref)

    assert embed.title == "Erreur"
    assert f"Je n'ai pas trouvé le scrutin {code_ref}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR



@pytest.mark.parametrize("code_ref", [("456")])
@patch('os.listdir', return_value=[])
@patch('utils.scrutinManager.Scrutin.from_json_by_ref', return_value=None)
def test_scr_handler_no_files(_mock_listdir, _mock_scrutin, code_ref):
    embed = scr_handler(code_ref)

    assert embed.title == "Erreur"
    assert f"Je n'ai pas trouvé le scrutin {code_ref}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR


@pytest.mark.parametrize("code_ref", [("456")])
@patch('os.listdir', return_value=["scrutin_456.json"])
@patch('utils.scrutinManager.Scrutin.from_json_by_ref', side_effect=lambda data, ref: mock_scrutin_adopte())
@patch('builtins.open', mock_open(read_data='not json'))
def test_scr_handler_malformed_json(_mock_scrutin, _mock_listdir, code_ref):
    embed = scr_handler(code_ref)

    assert embed.title == "Erreur"
    assert f"Je n'ai pas trouvé le scrutin {code_ref}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR
