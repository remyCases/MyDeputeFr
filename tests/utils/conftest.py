# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from pathlib import Path
from typing import Collection, Dict, Iterator, List, Union
from unittest.mock import MagicMock, mock_open, patch
import json
import pytest

from utils.deputeManager import Depute


JSON_DEPUTE = Dict[
    str, Dict[str, Union[
            Dict[str, str],
            Dict[str, Dict[str, str]],
            Dict[str, List[object]]
            ]]]

JSON_SCRUTIN = Dict[
    str, Dict[str, Union[
            str,
            Dict[str, str],
            Dict[str, Dict[str, str]],
            Dict[str, Collection[str]],
            Dict[str, Dict[str, Dict[str, List[Dict[str, Collection[str]]]]]]
            ]]]

sample_gp_data = {
    "organe": {
        "libelle": "Groupe Test"
    }
}


@pytest.fixture
def mocked_gp_file() -> Iterator[MagicMock]:
    m_open: MagicMock = mock_open(read_data=json.dumps(sample_gp_data))
    with patch("builtins.open", m_open):
        yield m_open


@pytest.fixture
def mocked_organe_folder(tmp_path: Path) -> Path:
    test_folder: Path = tmp_path / "organes"
    test_folder.mkdir()
    return test_folder


@pytest.fixture
def sample_scrutin_data_json() -> JSON_SCRUTIN:
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
def sample_valid_depute_dataclass() -> Depute:
    """Sample dataclass Depute"""
    return Depute(
        ref="PA456",
        last_name="Durand",
        first_name="Claire",
        dep="75",
        dep_name="Paris",
        circo="1",
        gp_ref="GP001",
        gp="Groupe Test"
    )

@pytest.fixture
def sample_valid_depute_json() -> JSON_DEPUTE:
    """Sample JSON data mimicking structure from your Depute.from_json"""
    return {
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
                                "departement": "Paris",
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

@pytest.fixture
def sample_missing_organe_depute_json() -> JSON_DEPUTE:
    """Sample JSON data mimicking structure from your Depute.from_json
    with a missing organe field"""
    return {
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
                                "departement": "Paris",
                                "numCirco": "1"
                            }
                        }
                    },
                    {
                        "typeOrgane": "GP",
                        "organes": {
                            "organeRef": ""
                        }
                    }
                ]
            }
        }
    }

@pytest.fixture
def sample_invalid_depute_json() -> JSON_DEPUTE:
    """Sample JSON data mimicking structure from your Depute.from_json
    with a missing organe field"""
    return {
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
                                "departement": "Paris",
                                "numCirco": "1"
                            }
                        }
                    },
                    {
                        "typeOrgane": "GP",
                        "organes": {
                            "organeRef": "INVALID"
                        }
                    }
                ]
            }
        }
    }
