# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from datetime import datetime
from typing import Optional
from unittest.mock import MagicMock
import pytest

from tests.utils.conftest import JSON_SCRUTIN
from utils.deputeManager import Depute
from utils.scrutinManager import Scrutin, ResultBallot


def test_from_json(
    mock_log: MagicMock,
    sample_scrutin_data_json: JSON_SCRUTIN,
    mock_bot: MagicMock) -> None:

    scrutin: Scrutin = Scrutin.from_json(sample_scrutin_data_json)

    # Assertions result
    assert scrutin.ref == "1001"
    assert scrutin.titre.startswith("Projet de loi")
    assert scrutin.dateScrutin ==  datetime(2025, 3, 12).date()
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
    mock_log: MagicMock,
    sample_scrutin_data_json: JSON_SCRUTIN,
    mock_bot: MagicMock) -> None:

    scrutin: Optional[Scrutin] = Scrutin.from_json_by_ref(sample_scrutin_data_json, "1001")

    # Assertions result
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
    mock_log: MagicMock,
    sample_scrutin_data_json: JSON_SCRUTIN,
    mock_bot: MagicMock) -> None:

    scrutin: Optional[Scrutin] = Scrutin.from_json_by_ref(sample_scrutin_data_json, "9999")

    # Assertions result
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
    mock_log: MagicMock,
    sample_scrutin_data_json: JSON_SCRUTIN,
    sample_valid_depute_dataclass: Depute,
    mock_bot: MagicMock) -> None:

    scrutin: Scrutin = Scrutin.from_json(sample_scrutin_data_json)
    result: Optional[ResultBallot] = scrutin.result(sample_valid_depute_dataclass)

    # Assertions result
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
    mock_log: MagicMock,
    sample_scrutin_data_json: JSON_SCRUTIN,
    ref: str,
    expected_result: ResultBallot,
    mock_bot: MagicMock) -> None:

    depute: Depute = Depute(
        ref=ref,
        last_name="Test",
        first_name="Test",
        dep="00",
        dep_name="Department test",
        circo="1",
        gp_ref="GP001",
        gp="Groupe Test"
    )
    scrutin: Scrutin = Scrutin.from_json(sample_scrutin_data_json)
    result: Optional[ResultBallot] = scrutin.result(depute)

    # Assertions result
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
    mock_log: MagicMock,
    sample_scrutin_data_json: JSON_SCRUTIN,
    mock_bot: MagicMock) -> None:

    scrutin: Scrutin = Scrutin.from_json(sample_scrutin_data_json)
    s: str = scrutin.to_string()

    # Assertions result
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
    mock_log: MagicMock,
    sample_scrutin_data_json: JSON_SCRUTIN,
    sample_valid_depute_dataclass: Depute,
    mock_bot: MagicMock) -> None:

    scrutin: Scrutin = Scrutin.from_json(sample_scrutin_data_json)
    msg: Optional[str] = scrutin.to_string_depute(sample_valid_depute_dataclass)

    # Assertions result
    assert msg is not None
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
    mock_log: MagicMock,
    sample_scrutin_data_json: JSON_SCRUTIN,
    mock_bot: MagicMock) -> None:

    scrutin: Scrutin = Scrutin.from_json(sample_scrutin_data_json)
    depute: Depute = Depute(
        ref="PA999",
        last_name="Martin",
        first_name="Sophie",
        dep="34",
        dep_name="Departement Test",
        circo="2",
        gp_ref="GP001",
        gp="Groupe Test"
    )
    msg: Optional[str] = scrutin.to_string_depute(depute)

    # Assertions result
    assert msg is not None
    assert "**absent**" in msg

    # Assertions logs
    mock_log.info.assert_not_called()
    mock_log.error.assert_not_called()
    mock_log.warning.assert_not_called()

    # Assertions bot
    mock_bot.assert_not_called()
    mock_bot.update_lock.__aenter__.assert_not_called()
    mock_bot.update_lock.__aexit__.assert_not_called()
