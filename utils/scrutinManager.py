# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing_extensions import Self

from attrs import define

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
    dateScrutin: datetime
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
        dateScrutin: datetime = datetime.strptime(data["scrutin"]["dateScrutin"], "%Y-%m-%d").date()
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


    def result(self, depute: Depute) -> ResultBallot | None:
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


    def to_string(self) -> str:
        return  f"Scrutin nº{self.ref}, le {self.dateScrutin}, {self.titre[:-1]} est {self.sort}." \
                f"Nombre de votants: {self.nombreVotants}\n" \
                f"Non votants: {self.nonVotant}\n" \
                f"Non votants volontaires: {self.nonVotantsVolontaire}" \
                f"Pour: {self.pour}\n" \
                f"Contre: {self.contre}\n" \
                f"Abstentions: {self.abstention}"

    def to_string_depute(self, depute: Depute) -> str | None:
        if self.result(depute) == ResultBallot.ABSENT:
            res = "absent"
        elif self.result(depute) == ResultBallot.NONVOTANT:
            res = "non votant"
        elif self.result(depute) == ResultBallot.POUR:
            res = "pour"
        elif self.result(depute) == ResultBallot.CONTRE:
            res = "contre"
        elif self.result(depute) == ResultBallot.ABSTENTION:
            res = "abstention"
        else:
            res = None

        return f"{depute.to_string()[:-1]} a voté **{res}** lors scrutin {self.ref} {self.sort} du {self.dateScrutin} concernant {self.titre}"


    def depute_vote(self, depute: Depute) -> ResultBallot:
        return self.result(depute)