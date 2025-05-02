# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import pytest

from utils.deputeManager import Depute
from utils.scrutinManager import Scrutin, ResultBallot


def test_from_json(
    sample_scrutin_data_json,
    mock_log,
    mock_bot):

    scrutin = Scrutin.from_json(sample_scrutin_data_json)

    assert scrutin.ref == "1001"
    assert scrutin.titre.startswith("Projet de loi")
    assert scrutin.dateScrutin == "2025-03-12"
    assert scrutin.sort == "Adopté"
    assert scrutin.nombreVotants == "577"
    assert scrutin.groupes["GP001"]["pour"] == ["PA456"]

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


def test_from_json_by_ref_match(
    sample_scrutin_data_json,
    mock_log,
    mock_bot):

    scrutin = Scrutin.from_json_by_ref(sample_scrutin_data_json, "1001")
    assert scrutin is not None
    assert scrutin.ref == "1001"

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


def test_from_json_by_ref_no_match(
    sample_scrutin_data_json,
    mock_log,
    mock_bot):

    scrutin = Scrutin.from_json_by_ref(sample_scrutin_data_json, "9999")
    assert scrutin is None

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


def test_result_pour(
    sample_scrutin_data_json,
    sample_valid_depute_dataclass,
    mock_log,
    mock_bot):

    scrutin = Scrutin.from_json(sample_scrutin_data_json)
    result = scrutin.result(sample_valid_depute_dataclass)
    assert result == ResultBallot.POUR

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


@pytest.mark.parametrize("ref, expected_result", [
    ("PA123", ResultBallot.NONVOTANT),
    ("PA456", ResultBallot.POUR),
    ("PA789", ResultBallot.CONTRE),
    ("PA321", ResultBallot.ABSTENTION),
    ("PA999", ResultBallot.ABSENT),
])
def test_result_variants(
    sample_scrutin_data_json,
    ref,
    expected_result,
    mock_log,
    mock_bot):

    depute = Depute(
        ref=ref,
        last_name="Test",
        first_name="Test",
        dep="00",
        dep_name="Department test",
        circo="1",
        gp_ref="GP001",
        gp="Groupe Test"
    )
    scrutin = Scrutin.from_json(sample_scrutin_data_json)
    result = scrutin.result(depute)
    assert result == expected_result

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


def test_to_string(
    sample_scrutin_data_json,
    mock_log,
    mock_bot):

    scrutin = Scrutin.from_json(sample_scrutin_data_json)
    s = scrutin.to_string()
    assert "Scrutin nº1001" in s
    assert "le 2025-03-12" in s
    assert "Nombre de votants: 577" in s

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


def test_to_string_depute_pour(
    sample_scrutin_data_json,
    sample_valid_depute_dataclass,
    mock_log,
    mock_bot):

    scrutin = Scrutin.from_json(sample_scrutin_data_json)
    msg = scrutin.to_string_depute(sample_valid_depute_dataclass)
    assert "**pour**" in msg
    assert "scrutin 1001" in msg

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()


def test_to_string_depute_absent(
    sample_scrutin_data_json,
    mock_log,
    mock_bot):

    scrutin = Scrutin.from_json(sample_scrutin_data_json)
    depute = Depute(
        ref="PA999",
        last_name="Martin",
        first_name="Sophie",
        dep="34",
        dep_name="Departement Test",
        circo="2",
        gp_ref="GP001",
        gp="Groupe Test"
    )
    msg = scrutin.to_string_depute(depute)
    assert "**absent**" in msg

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()
