# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
import json
from typing import Self
from attrs import define
from config.config import ORGANE_FOLDER

@define(kw_only=True)
class Depute:
    ref: str
    last_name: str
    first_name: str
    dep: str
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
            circo=circo,
            gp_ref=gp_ref,
            gp=gp,
        )

    @classmethod
    def from_json_by_name(cls, data: dict, name: str) -> Self | None:
        last_name: str = data["acteur"]["etatCivil"]["ident"]["nom"].replace(" ", "")
        if name.lower() != last_name.lower():
            return None
        return Depute.from_json(data)

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

    def to_string(self) -> str:
        return f"Ton député est {self.to_string_less()}."

    def to_string_less(self) -> str:
        return f"{self.first_name} {self.last_name} élu dans le {self.dep}-{self.circo} dans le groupe {self.gp}"