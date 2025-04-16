# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
import pathlib
from unittest.mock import MagicMock, patch

import pytest

DATA_TEST = os.path.join(pathlib.Path(__file__).parent.resolve(), "..", "data", "2024-04-07")
DATA_TEST_SCRUTINS= os.path.join(DATA_TEST, 'scrutins')
DATA_TEST_ACTEUR = os.path.join(DATA_TEST, 'acteur')
DATA_TEST_ORGANE = os.path.join(DATA_TEST, 'organe')

@pytest.fixture()
def mock_folder_paths():
    with (
        patch('handlers.deputeHandler.SCRUTINS_FOLDER', DATA_TEST_SCRUTINS),
        patch('handlers.deputeHandler.ACTEUR_FOLDER', DATA_TEST_ACTEUR),
        patch('utils.deputeManager.ORGANE_FOLDER', DATA_TEST_ORGANE)
    ):
        yield


@pytest.fixture(params=[
    ("Panot", "Mathilde Panot"),
    ("PaNoT", "Mathilde Panot"),
    ("Le Pen", "Marine Le Pen"),
    ("LePen", "Marine Le Pen"),
    ("Trébuchet", "Vincent Trébuchet"),
    ("Trebuchet", "Vincent Trébuchet"),
    ("Thiébault-Martinez", "Céline Thiébault-Martinez"),
    ("Thiébault Martinez", "Céline Thiébault-Martinez"),
    ("Thiebault Martinez", "Céline Thiébault-Martinez"),
    ("ThiebaultMartinez", "Céline Thiébault-Martinez"),
    ("D'Intorni", "Christelle D'Intorni"),
    ("D Intorni", "Christelle D'Intorni"),
    ("DIntorni", "Christelle D'Intorni")
])
def valid_name(request):
    return request.param

@pytest.fixture(params=["Unknown", "Fictitious Name"])
def invalid_name(request):
    return request.param