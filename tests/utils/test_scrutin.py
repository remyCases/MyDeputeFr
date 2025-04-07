# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import pytest

from utils.deputeManager import Depute
from utils.scrutinManager import Scrutin, ResultBallot


@pytest.fixture
def sample_scrutin_data():
    return {
        "scrutin": {
            "numero": "1001",
            "titre": "Projet de loi sur l'énergie renouvelable.",
            "dateScrutin": "2025-03-12",
            "sort": {"code": "Adopté"},
            "syntheseVote": {
                "nombreVotants": "577",
                "decompte": {
                    "nonVotants": "50",
                    "pour": "300",
                    "contre": "200",
                    "abstentions": "27",
                    "nonVotantsVolontaires": "15"
                }
            },
            "ventilationVotes": {
                "organe": {
                    "groupes": {
                        "groupe": [
                            {
                                "organeRef": "GP001",
                                "vote": {
                                    "decompteNominatif": {
                                        "nonVotants": {"votant": {"acteurRef": "PA123"}},
                                        "pours": {"votant": [{"acteurRef": "PA456"}]},
                                        "contres": {"votant": [{"acteurRef": "PA789"}]},
                                        "abstentions": {"votant": {"acteurRef": "PA321"}}
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }
    }

@pytest.fixture
def sample_depute():
    return Depute(
        ref="PA456",
        last_name="Durand",
        first_name="Claire",
        dep="75",
        circo="1",
        gp_ref="GP001",
        gp="Groupe Test"
    )

def test_from_json(sample_scrutin_data):
    scrutin = Scrutin.from_json(sample_scrutin_data)

    assert scrutin.ref == "1001"
    assert scrutin.titre.startswith("Projet de loi")
    assert scrutin.dateScrutin == "2025-03-12"
    assert scrutin.sort == "Adopté"
    assert scrutin.nombreVotants == "577"
    assert scrutin.groupes["GP001"]["pour"] == ["PA456"]


def test_from_json_by_ref_match(sample_scrutin_data):
    scrutin = Scrutin.from_json_by_ref(sample_scrutin_data, "1001")
    assert scrutin is not None
    assert scrutin.ref == "1001"


def test_from_json_by_ref_no_match(sample_scrutin_data):
    scrutin = Scrutin.from_json_by_ref(sample_scrutin_data, "9999")
    assert scrutin is None


def test_result_pour(sample_scrutin_data, sample_depute):
    scrutin = Scrutin.from_json(sample_scrutin_data)
    result = scrutin.result(sample_depute)
    assert result == ResultBallot.POUR


@pytest.mark.parametrize("ref, expected_result", [
    ("PA123", ResultBallot.NONVOTANT),
    ("PA456", ResultBallot.POUR),
    ("PA789", ResultBallot.CONTRE),
    ("PA321", ResultBallot.ABSTENTION),
    ("PA999", ResultBallot.ABSENT),
])
def test_result_variants(sample_scrutin_data, ref, expected_result):
    depute = Depute(
        ref=ref,
        last_name="Test",
        first_name="Test",
        dep="00",
        circo="1",
        gp_ref="GP001",
        gp="Groupe Test"
    )
    scrutin = Scrutin.from_json(sample_scrutin_data)
    result = scrutin.result(depute)
    assert result == expected_result


def test_to_string(sample_scrutin_data):
    scrutin = Scrutin.from_json(sample_scrutin_data)
    s = scrutin.to_string()
    assert "Scrutin nº1001" in s
    assert "le 2025-03-12" in s
    assert "Nombre de votants: 577" in s


def test_to_string_depute_pour(sample_scrutin_data, sample_depute):
    scrutin = Scrutin.from_json(sample_scrutin_data)
    msg = scrutin.to_string_depute(sample_depute)
    assert "**pour**" in msg
    assert "scrutin 1001" in msg


def test_to_string_depute_absent(sample_scrutin_data):
    scrutin = Scrutin.from_json(sample_scrutin_data)
    depute = Depute(
        ref="PA999",
        last_name="Martin",
        first_name="Sophie",
        dep="34",
        circo="2",
        gp_ref="GP001",
        gp="Groupe Test"
    )
    msg = scrutin.to_string_depute(depute)
    assert "**absent**" in msg

