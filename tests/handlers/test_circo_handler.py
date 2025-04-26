from unittest.mock import MagicMock, patch, mock_open
import pytest
from discord import Embed

from config.config import DISCORD_EMBED_COLOR_MSG, DISCORD_EMBED_COLOR_ERR
from handlers.deputeHandler import ciro_handler

def mock_depute():
    depute = MagicMock()
    depute.first_name = "Jean"
    depute.last_name = "Dupont"
    depute.url = "http://example.com"
    depute.image = "http://example.com/image.jpg"
    depute.dep = "93"
    depute.circo = "10"
    depute.dep_name = "Paris"
    depute.gp = "La République En Marche"
    return depute


@pytest.mark.parametrize("code_dep, code_circo", [
    ("93", "10"),
])
@patch('os.listdir', return_value=["depute_data_01_01.json", "depute_data_93_10.json", "depute_data_99_20.json"])
@patch('utils.deputeManager.Depute.from_json_by_circo', side_effect=lambda data, code_dep, code_circo: mock_depute() if '93' == code_dep and '10' == code_circo else None)
@patch('builtins.open', mock_open(read_data='{}'))
def test_ciro_handler_found(_mock_list_dir, _mock_from_json_by_circo, code_dep, code_circo):
    # Call the handler
    embed = ciro_handler(code_dep, code_circo)

    # Assert the result
    assert isinstance(embed, Embed)
    assert embed.title == ":bust_in_silhouette: Jean Dupont"
    assert ":round_pushpin: **Circoncription** : 93-10 (Paris)\n:classical_building: **Groupe** : La République En Marche" == embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_MSG


# Test for when no deputy is found (empty result)
@pytest.mark.parametrize("code_dep, code_circo", [
    ("00", "00"),
    ("AB", "CD"),
])
@patch('os.listdir', return_value=["depute_data_01_01.json", "depute_data_93_10.json", "depute_data_99_20.json"])
@patch('utils.deputeManager.Depute.from_json_by_circo', return_value=None)
@patch('builtins.open', mock_open(read_data='{}'))
def test_ciro_handler_not_found(_mock_list_dir, _mock_from_json_by_circo, code_dep, code_circo):
    # Call the handler
    embed = ciro_handler(code_dep, code_circo)

    # Assert the error
    assert embed.title == "Député non trouvé"
    assert f"Je n'ai pas trouvé de député dans le {code_dep}-{code_circo}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR


@pytest.mark.parametrize("code_dep, code_circo", [
    ("93", "10"),
])
@patch('os.listdir', return_value=[])
@patch('utils.deputeManager.Depute.from_json_by_circo', side_effect=lambda data, code_dep, code_circo: mock_depute() if '93' == code_dep and '10' == code_circo else None)
def test_ciro_handler_no_files(_mock_list_dir, _mock_from_json_by_circo, code_dep, code_circo):
    # Call the handler
    embed = ciro_handler(code_dep, code_circo)

    # Assert the error
    assert embed.title == "Député non trouvé"
    assert f"Je n'ai pas trouvé de député dans le {code_dep}-{code_circo}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR


@pytest.mark.parametrize("code_dep, code_circo", [
    ("93", "10"),
])
@patch('os.listdir', return_value=["depute_data_01_01.json", "depute_data_93_10.json", "depute_data_99_20.json"])
@patch('utils.deputeManager.Depute.from_json_by_circo', side_effect=lambda data, code_dep, code_circo: mock_depute() if '93' == code_dep and '10' == code_circo else None)
def test_ciro_handler_read_errors(_mock_list_dir, _mock_from_json_by_circo, code_dep, code_circo):
    # Call the handler
    embed = ciro_handler(code_dep, code_circo)

    # Assert the error
    assert embed.title == "Député non trouvé"
    assert f"Je n'ai pas trouvé de député dans le {code_dep}-{code_circo}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR

@pytest.mark.parametrize("code_dep, code_circo", [
    ("93", "10"),
])
@patch('os.listdir', return_value=["depute_data_01_01.json", "depute_data_93_10.json", "depute_data_99_20.json"])
@patch('utils.deputeManager.Depute.from_json_by_circo', side_effect=lambda data, code_dep, code_circo: mock_depute() if '93' == code_dep and '10' == code_circo else None)
@patch('builtins.open', mock_open(read_data='not json'))
def test_ciro_handler_json_errors(_mock_list_dir, _mock_from_json_by_circo, code_dep, code_circo):
    # Call the handler
    embed = ciro_handler(code_dep, code_circo)

    # Assert the error
    assert embed.title == "Député non trouvé"
    assert f"Je n'ai pas trouvé de député dans le {code_dep}-{code_circo}." in embed.description
    assert int(embed.color) == DISCORD_EMBED_COLOR_ERR
