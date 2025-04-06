# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

import os
from typing import Self
from enum import Enum
from attrs import define
from dotenv import load_dotenv

from utils.deputeManager import Depute

# class syntax

class ResultBallot(Enum):
    ABSENT = 0
    NONVOTANT = 1
    POUR = 2
    CONTRE = 3
    ABSTENTION = 4

@define(kw_only=True)
class Scrutin:
    ref: str
    titre: str
    dateScrutin: str
    sort: str
    nombreVotants: str
    nonVotant: str
    pour: str
    contre: str
    abstention: str
    nonVotantsVolontaire: str
    groupes: dict

    @classmethod
    def from_json(cls, data: dict) -> Self:
        ref: str = data["scrutin"]["numero"]
        titre: str = data["scrutin"]["titre"]
        dateScrutin: str = data["scrutin"]["dateScrutin"]
        sort: str = data["scrutin"]["sort"]["code"]
        nombreVotants: str = data["scrutin"]["syntheseVote"]["nombreVotants"]
        nonVotant: str = data["scrutin"]["syntheseVote"]["decompte"]["nonVotants"]
        pour: str = data["scrutin"]["syntheseVote"]["decompte"]["pour"]
        contre: str = data["scrutin"]["syntheseVote"]["decompte"]["contre"]
        abstention: str = data["scrutin"]["syntheseVote"]["decompte"]["abstentions"]
        nonVotantsVolontaire: str = data["scrutin"]["syntheseVote"]["decompte"]["nonVotantsVolontaires"]

        groupes: dict = data["scrutin"]["ventilationVotes"]["organe"]["groupes"]["groupe"]
        groupes_scrutin: dict = {}
        for groupe in groupes:
            organe_ref: str = groupe["organeRef"]
            nv_list: list = []
            p_list: list = []
            c_list: list = []
            a_list: list = []

            nonVotants = groupe["vote"]["decompteNominatif"]["nonVotants"]
            if nonVotants:
                nonVotants = nonVotants["votant"]
                if isinstance(nonVotants, list):
                    for nv in nonVotants:
                        nv_list.append(nv["acteurRef"])
                else:
                    nv_list.append(nonVotants["acteurRef"])

            pours = groupe["vote"]["decompteNominatif"]["pours"]
            if pours:
                pours = pours["votant"]
                if isinstance(pours, list):
                    for p in pours:
                        p_list.append(p["acteurRef"])
                else:
                    p_list.append(pours["acteurRef"])

            contres = groupe["vote"]["decompteNominatif"]["contres"]
            if contres:
                contres = contres["votant"]
                if isinstance(contres, list):
                    for c in contres:
                        c_list.append(c["acteurRef"])
                else:
                    c_list.append(contres["acteurRef"])

            abstentions = groupe["vote"]["decompteNominatif"]["abstentions"]
            if abstentions:
                abstentions = abstentions["votant"]
                if isinstance(abstentions, list):
                    for a in abstentions:
                        a_list.append(a["acteurRef"])
                else:
                    a_list.append(abstentions["acteurRef"])

            groupes_scrutin[organe_ref] = {
                "nonVotant": nv_list,
                "pour": p_list,
                "contre": c_list,
                "abstention": a_list,
            }

        return cls(
            ref=ref,
            titre=titre,
            dateScrutin=dateScrutin,
            sort=sort,
            nombreVotants=nombreVotants,
            nonVotant=nonVotant,
            pour=pour,
            contre=contre,
            abstention=abstention,
            nonVotantsVolontaire=nonVotantsVolontaire,
            groupes=groupes_scrutin,
        )
    
    @classmethod
    def from_json_by_ref(cls, data: dict, code_ref: str) -> Self | None:
        ref: str = data["scrutin"]["numero"]
        if ref != code_ref:
            return None
        return Scrutin.from_json(data)
    
    def to_string(self) -> str:
        return f"Le {self.dateScrutin}, {self.sort}:\n{self.titre}\n\n  \
            Nombre de votants: {self.nombreVotants}.\n                  \
            Non votants: {self.nonVotant}.\n                            \
            Pour: {self.pour}.\n                                        \
            Contre: {self.contre}.\n                                    \
            Abstentions: {self.abstention}.\n                           \
            Non votants volontaires: {self.nonVotantsVolontaire}."
    
    def result(self, depute: Depute) -> ResultBallot:

        for gp_ref, groupe in self.groupes.items():
            if depute.gp_ref != gp_ref:
                continue

            if depute.ref in groupe["nonVotant"]:
                return ResultBallot.NONVOTANT

            if depute.ref in groupe["pour"]:
                return ResultBallot.POUR

            if depute.ref in groupe["contre"]:
                return ResultBallot.CONTRE

            if depute.ref in groupe["abstention"]:
                return ResultBallot.ABSTENTION

            return ResultBallot.ABSENT

    def to_string_depute(self, depute: Depute) -> str:
        match self.result(depute):
            case ResultBallot.ABSENT:
                res = "absent"
            case ResultBallot.NONVOTANT:
                res = "non votant"
            case ResultBallot.POUR:
                res = "pour"
            case ResultBallot.CONTRE:
                res = "contre"
            case ResultBallot.ABSTENTION:
                res = "abstention"

        return f"{depute.to_string_less()}\na voté **{res}** lors du \n{self.dateScrutin}, {self.sort}:\n{self.titre}"
