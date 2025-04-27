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


@define(kw_only=True)
class Depute:
    ref: str
    last_name: str
    first_name: str
    dep: str
    dep_name: str
    circo: str
    gp_ref: str
    gp: str

    @classmethod
    def from_json(cls, data: dict) -> Self:
        ref: str = data["acteur"]["uid"]["#text"]
        last_name: str = data["acteur"]["etatCivil"]["ident"]["nom"]
        first_name: str = data["acteur"]["etatCivil"]["ident"]["prenom"]
        mandats: dict = data["acteur"]["mandats"]["mandat"]

        elec: str = ""
        gp_ref: str = ""
        gp: str = ""
        dep: str = ""
        dep_name: str = ""
        circo: str = ""
        elec_found = False
        gp_found = False
        for mandat in mandats:
            if not elec_found and "election" in mandat:
                elec = mandat["election"]
                if elec["causeMandat"]:
                    if isinstance(elec["causeMandat"], list) and "\u00e9lections g\u00e9n\u00e9rales" in elec["causeMandat"]:
                        elec_found = True
                    elif "\u00e9lections g\u00e9n\u00e9rales" == elec["causeMandat"].lower():
                        elec_found = True
            if not gp_found and "typeOrgane" in mandat and "GP" == mandat["typeOrgane"]:
                gp_ref = mandat["organes"]["organeRef"]
                gp_found = True

        if elec:
            dep = elec["lieu"]["numDepartement"]
            dep_name = elec["lieu"]["departement"]
            circo = elec["lieu"]["numCirco"]

        if gp_ref:
            with open(os.path.join(ORGANE_FOLDER, f"{gp_ref}.json"), "r") as g:
                group: dict = json.load(g)
                gp: str = group["organe"]["libelle"]

        return cls(
            ref=ref,
            last_name=last_name,
            first_name=first_name,
            dep=dep,
            dep_name=dep_name,
            circo=circo,
            gp_ref=gp_ref,
            gp=gp,
        )


    @classmethod
    def from_json_by_ref(cls, data: dict, ref: str) -> Self | None:
        data_ref: str = data["acteur"]["uid"]["#text"]
        if data_ref == ref:
            return Depute.from_json(data)
        return None


    @classmethod
    def from_json_by_name(cls, data: dict, last_name: str, first_name: str | None = None) -> Self | None:
        def normalize_name(name: str) -> str:
            return re.sub(r'[^a-z]', '', unidecode(name).lower())
        data_last_name: str = data["acteur"]["etatCivil"]["ident"]["nom"]
        data_first_name: str = data["acteur"]["etatCivil"]["ident"]["prenom"]
        if normalize_name(last_name) == normalize_name(data_last_name):
            if first_name is None or normalize_name(first_name) == normalize_name(data_first_name):
                return Depute.from_json(data)
        return None

    @classmethod
    def from_json_by_dep(cls, data: dict, code_dep: str):
        mandats: dict = data["acteur"]["mandats"]["mandat"]

        elec: str = ""
        dep: str = ""
        for mandat in mandats:
            if "election" in mandat:
                elec = mandat["election"]
                if elec["causeMandat"]:
                    if isinstance(elec["causeMandat"], list) and "\u00e9lections g\u00e9n\u00e9rales" in elec["causeMandat"]:
                        break
                    elif "\u00e9lections g\u00e9n\u00e9rales" == elec["causeMandat"].lower():
                        break
        
        if elec:
            dep = elec["lieu"]["numDepartement"]
        else:
            return None
        if code_dep != dep:
            return None
        return Depute.from_json(data)
        
    @classmethod
    def from_json_by_circo(cls, data: dict, code_dep: str, code_circo: str) -> Self | None:
        mandats: dict = data["acteur"]["mandats"]["mandat"]

        elec: str = ""
        dep: str = ""
        circo: str = ""
        for mandat in mandats:
            if "election" in mandat:
                elec = mandat["election"]
                if elec["causeMandat"]:
                    if isinstance(elec["causeMandat"], list) and "\u00e9lections g\u00e9n\u00e9rales" in elec["causeMandat"]:
                        break
                    elif "\u00e9lections g\u00e9n\u00e9rales" == elec["causeMandat"].lower():
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
        return f"https://www.assemblee-nationale.fr/dyn/deputes/{self.ref}"

    @property
    def image(self) -> str:
        return f"https://www.assemblee-nationale.fr/dyn/static/tribun/17/photos/carre/{self.ref[2:]}.jpg"

    def to_string(self) -> str:
        return f"{self.first_name} {self.last_name} député élu de la circonscription {self.dep}-{self.circo} ({self.dep_name}) appartenant au groupe {self.gp}."
