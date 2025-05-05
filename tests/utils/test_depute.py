# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import json
from typing import Union
from unittest.mock import MagicMock, call, mock_open, patch

from tests.utils.conftest import JSON_DEPUTE, sample_gp_data
from utils.deputeManager import Depute


@patch("utils.deputeManager.logger")
@patch('builtins.open', mock_open(read_data=json.dumps(sample_gp_data)))
def test_from_json(
    mock_log: MagicMock,
    sample_valid_depute_json: JSON_DEPUTE,
    mock_bot: MagicMock) -> None:

    depute: Depute = Depute.from_json(sample_valid_depute_json)

    # Assertions result
    assert depute.ref == "PA123456"
    assert depute.last_name == "Dupont"
    assert depute.first_name == "Jean"
    assert depute.dep == "75"
    assert depute.circo == "1"
    assert depute.gp_ref == "ORG123"
    assert depute.gp == "Groupe Test"
    assert "assemblee-nationale.fr" in depute.url
    assert depute.ref[2:] in depute.image

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@patch("utils.deputeManager.logger")
@patch('builtins.open', mock_open(read_data=json.dumps(sample_gp_data)))
def test_missing_organe_from_json(
    mock_log: MagicMock,
    sample_missing_organe_depute_json: JSON_DEPUTE,
    mock_bot: MagicMock) -> None:

    depute: Depute = Depute.from_json(sample_missing_organe_depute_json)

    # Assertions result
    assert depute.ref == "PA123456"
    assert depute.last_name == "Dupont"
    assert depute.first_name == "Jean"
    assert depute.dep == "75"
    assert depute.circo == "1"
    assert depute.gp_ref == ""
    assert depute.gp == ""
    assert "assemblee-nationale.fr" in depute.url
    assert depute.ref[2:] in depute.image

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_has_calls([
        call("%s does not have any organe reference.", depute.ref)
    ])

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@patch("utils.deputeManager.logger")
@patch('builtins.open', return_value=mock_open())
def test_invalid_organe_from_json(
    mock_builtins_open: MagicMock,
    mock_log: MagicMock,
    sample_invalid_depute_json: JSON_DEPUTE,
    mock_bot: MagicMock) -> None:

    mock_builtins_open.side_effect = OSError
    depute: Depute = Depute.from_json(sample_invalid_depute_json)

    # Assertions result
    assert depute.ref == "PA123456"
    assert depute.last_name == "Dupont"
    assert depute.first_name == "Jean"
    assert depute.dep == "75"
    assert depute.circo == "1"
    assert depute.gp_ref == ""
    assert depute.gp == ""
    assert "assemblee-nationale.fr" in depute.url
    assert depute.ref[2:] in depute.image

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_has_calls([
        call("Cannot find the organe file %s for %s", "INVALID", depute.ref)
    ])

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@patch("utils.deputeManager.logger")
@patch('builtins.open', mock_open(read_data=json.dumps(sample_gp_data)))
def test_from_json_by_name_match(
    mock_log: MagicMock,
    sample_valid_depute_json: JSON_DEPUTE,
    mock_bot: MagicMock) -> None:

    depute: Union[Depute, None] = Depute.from_json_by_name(sample_valid_depute_json, "Dupont")

    # Assertions result
    assert depute is not None
    assert depute.last_name == "Dupont"

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@patch("utils.deputeManager.logger")
def test_from_json_by_name_no_match(
    mock_log: MagicMock,
    sample_valid_depute_json: JSON_DEPUTE,
    mock_bot: MagicMock) -> None:

    depute: Union[Depute, None] = Depute.from_json_by_name(sample_valid_depute_json, "Durand")

    # Assertions result
    assert depute is None

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@patch("utils.deputeManager.logger")
@patch('builtins.open', mock_open(read_data=json.dumps(sample_gp_data)))
def test_from_json_by_dep_match(
    mock_log: MagicMock,
    sample_valid_depute_json: JSON_DEPUTE,
    mock_bot: MagicMock) -> None:

    depute: Union[Depute, None] = Depute.from_json_by_dep(sample_valid_depute_json, "75")

    # Assertions result
    assert depute is not None
    assert depute.dep == "75"

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@patch("utils.deputeManager.logger")
def test_from_json_by_dep_no_match(
    mock_log: MagicMock,
    sample_valid_depute_json: JSON_DEPUTE,
    mock_bot: MagicMock) -> None:

    depute: Union[Depute, None] = Depute.from_json_by_dep(sample_valid_depute_json, "13")

    # Assertions result
    assert depute is None

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@patch("utils.deputeManager.logger")
@patch('builtins.open', mock_open(read_data=json.dumps(sample_gp_data)))
def test_from_json_by_circo_match(
    mock_log: MagicMock,
    sample_valid_depute_json: JSON_DEPUTE,
    mock_bot: MagicMock) -> None:

    depute: Union[Depute, None] = Depute.from_json_by_circo(sample_valid_depute_json, "75", "1")

    # Assertions result
    assert depute is not None
    assert depute.dep == "75"
    assert depute.circo == "1"

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@patch("utils.deputeManager.logger")
def test_from_json_by_circo_no_match(
    mock_log: MagicMock,
    sample_valid_depute_json: JSON_DEPUTE,
    mock_bot: MagicMock) -> None:

    depute: Union[Depute, None] = Depute.from_json_by_circo(sample_valid_depute_json, "75", "3")

    # Assertions result
    assert depute is None

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@patch("utils.deputeManager.logger")
@patch('builtins.open', mock_open(read_data=json.dumps(sample_gp_data)))
def test_to_string(
    mock_log: MagicMock,
    sample_valid_depute_json: JSON_DEPUTE,
    mock_bot: MagicMock) -> None:

    depute: Depute = Depute.from_json(sample_valid_depute_json)
    expected = "Jean Dupont député élu.e de la circonscription "\
        "75-1 (Paris) appartenant au groupe Groupe Test."

    # Assertions result
    assert depute.to_string() == expected

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()
