# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.
from __future__ import annotations

import json
import os
import re

from attrs import define
from typing_extensions import Self
from unidecode import unidecode

from config.config import ORGANE_FOLDER

ELECTION = "\u00e9lections g\u00e9n\u00e9rales"

@define(kw_only=True)
class Depute:
    """Dataclass for storing member of parliament's data"""

    ref: str
    last_name: str
    first_name: str
    dep: str
    circo: str
    gp_ref: str
    gp: str

    @classmethod
    def from_json(cls, data: dict) -> Self:
        """Convert json data into a Depute dataclass"""

        ref: str = data["acteur"]["uid"]["#text"]
        last_name: str = data["acteur"]["etatCivil"]["ident"]["nom"]
        first_name: str = data["acteur"]["etatCivil"]["ident"]["prenom"]
        mandats: dict = data["acteur"]["mandats"]["mandat"]

        elec: str = ""
        gp_ref: str = ""
        gp: str = ""
        dep: str = ""
        circo: str = ""
        elec_found: bool = False
        for mandat in mandats:
            if not elec_found and "election" in mandat:
                elec = mandat["election"]
                if elec["causeMandat"]:
                    if isinstance(elec["causeMandat"], list) and ELECTION in elec["causeMandat"]:
                        elec_found = True
                    elif ELECTION == elec["causeMandat"].lower():
                        elec_found = True
            if not gp_ref and "typeOrgane" in mandat and "GP" == mandat["typeOrgane"]:
                gp_ref = mandat["organes"]["organeRef"]

        if elec:
            dep = elec["lieu"]["numDepartement"]
            circo = elec["lieu"]["numCirco"]

        if gp_ref:
            organe_file = ORGANE_FOLDER / f"{gp_ref}.json"
            try:
                with open(organe_file, "r", encoding="utf-8") as g:
                    gp: str = json.load(g)["organe"]["libelle"]
            except OSError:
                print(f"The file {organe_file} was not found.")
                gp = ""
                gp_ref = ""
        else:
            print("The file was not found.")

        return cls(
            ref=ref,
            last_name=last_name,
            first_name=first_name,
            dep=dep,
            circo=circo,
            gp_ref=gp_ref,
            gp=gp,
        )

    @classmethod
    def from_json_by_name(cls, data: dict, name: str) -> Self | None:
        """Return a Depute dataclass if input json matches the given name"""

        def normalize_name(name: str) -> str:
            return re.sub(r'[^a-z]', '', unidecode(name).lower())

        last_name: str = data["acteur"]["etatCivil"]["ident"]["nom"]
        if normalize_name(name) != normalize_name(last_name) :
            return None
        return Depute.from_json(data)

    @classmethod
    def from_json_by_dep(cls, data: dict, code_dep: str) -> Self | None:
        """Return a Depute dataclass if input json matches the given administrative division"""

        mandats: dict = data["acteur"]["mandats"]["mandat"]
        elec: str = ""
        for mandat in mandats:
            if "election" in mandat:
                elec = mandat["election"]
                if elec["causeMandat"]:
                    if isinstance(elec["causeMandat"], list) and ELECTION in elec["causeMandat"]:
                        break
                    if ELECTION == elec["causeMandat"].lower():
                        break

        if not elec or elec["lieu"]["numDepartement"] != code_dep:
            return None
        return Depute.from_json(data)

    @classmethod
    def from_json_by_circo(cls, data: dict, code_dep: str, code_circo: str) -> Self | None:
        """Return a Depute dataclass if input json matches the given admin and sub-admin division"""

        mandats: dict = data["acteur"]["mandats"]["mandat"]
        elec: str = ""
        dep: str = ""
        circo: str = ""
        for mandat in mandats:
            if "election" in mandat:
                elec = mandat["election"]
                if elec["causeMandat"]:
                    if isinstance(elec["causeMandat"], list) and ELECTION in elec["causeMandat"]:
                        break
                    elif ELECTION == elec["causeMandat"].lower():
                        break
        if elec:
            dep = elec["lieu"]["numDepartement"]
            circo = elec["lieu"]["numCirco"]
        else:
            return None
        if (code_dep != dep) or (circo != code_circo):
            return None
        return Depute.from_json(data)

    @property
    def url(self) -> str:
        """Return the url associated to a member of parliament"""
        return f"https://www.assemblee-nationale.fr/dyn/deputes/{self.ref}"

    @property
    def image(self) -> str:
        """Return the official picture of a member of parliament"""
        ref = self.ref[2:]
        return f"https://www.assemblee-nationale.fr/dyn/static/tribun/17/photos/carre/{ref}.jpg"

    def to_string(self) -> str:
        """Format a member of parliament data into a string"""
        return f"{self.first_name} {self.last_name} député élu.e \
de la circonscription {self.dep}-{self.circo} \
appartenant au groupe {self.gp}."
