# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.
#

# TODO Test if acteurs found but no organes
# TODO Test if acteurs found but no organes file is found
# TODO Check if actuerus can have multiple organes, then add test it if it the case

import pytest
import json
from unittest.mock import mock_open, patch

from utils.deputeManager import Depute

# Sample JSON data mimicking structure from your Depute.from_json
sample_depute_data = {
    "acteur": {
        "uid": {"#text": "PA123456"},
        "etatCivil": {
            "ident": {
                "nom": "Dupont",
                "prenom": "Jean"
            }
        },
        "mandats": {
            "mandat": [
                {
                    "election": {
                        "causeMandat": "élections générales",
                        "lieu": {
                            "numDepartement": "75",
                            "numCirco": "1"
                        }
                    }
                },
                {
                    "typeOrgane": "GP",
                    "organes": {
                        "organeRef": "ORG123"
                    }
                }
            ]
        }
    }
}

sample_gp_data = {
    "organe": {
        "libelle": "Groupe Test"
    }
}


@pytest.fixture
def mocked_gp_file():
    m_open = mock_open(read_data=json.dumps(sample_gp_data))
    with patch("builtins.open", m_open):
        yield m_open


@pytest.fixture
def mocked_organe_folder(tmp_path):
    test_folder = tmp_path / "organes"
    test_folder.mkdir()
    return test_folder

@patch('builtins.open', mock_open(read_data=json.dumps(sample_gp_data)))
def test_from_json(mocked_gp_file, mocked_organe_folder):
    depute = Depute.from_json(sample_depute_data)

    assert depute.ref == "PA123456"
    assert depute.last_name == "Dupont"
    assert depute.first_name == "Jean"
    assert depute.dep == "75"
    assert depute.circo == "1"
    assert depute.gp_ref == "ORG123"
    assert depute.gp == "Groupe Test"
    assert "assemblee-nationale.fr" in depute.url
    assert depute.ref[2:] in depute.image

@patch('builtins.open', mock_open(read_data=json.dumps(sample_gp_data)))
def test_from_json_by_name_match(mocked_organe_folder):
    depute = Depute.from_json_by_name(sample_depute_data, "Dupont")
    assert depute is not None
    assert depute.last_name == "Dupont"


def test_from_json_by_name_no_match():
    depute = Depute.from_json_by_name(sample_depute_data, "Durand")
    assert depute is None

@patch('builtins.open', mock_open(read_data=json.dumps(sample_gp_data)))
def test_from_json_by_dep_match(mocked_organe_folder):
    depute = Depute.from_json_by_dep(sample_depute_data, "75")
    assert depute is not None
    assert depute.dep == "75"


def test_from_json_by_dep_no_match():
    depute = Depute.from_json_by_dep(sample_depute_data, "13")
    assert depute is None

@patch('builtins.open', mock_open(read_data=json.dumps(sample_gp_data)))
def test_from_json_by_circo_match(mocked_organe_folder):
    depute = Depute.from_json_by_circo(sample_depute_data, "75", "1")
    assert depute is not None
    assert depute.dep == "75"
    assert depute.circo == "1"


def test_from_json_by_circo_no_match():
    depute = Depute.from_json_by_circo(sample_depute_data, "75", "3")
    assert depute is None

@patch('builtins.open', mock_open(read_data=json.dumps(sample_gp_data)))
def test_to_string(mocked_organe_folder):
    depute = Depute.from_json(sample_depute_data)
    expected = "Jean Dupont député élu de la circonscription 75-1 appartenant au groupe Groupe Test."
    assert depute.to_string() == expected



