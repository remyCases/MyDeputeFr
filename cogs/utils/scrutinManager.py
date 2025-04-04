# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of StatisticalAgreement project from https://github.com/remyCases/StatisticalAgreement.

from typing import Self
from attrs import define

from .deputeManager import Depute

SCRUTINS_FOLDER = "Scrutins\\json"

@define(kw_only=True)
class Scrutin:
    ref: str
    titre: str
    dateScrutin: str
    sort: str
    nombreVotants: str
    nonVotants: str
    pour: str
    contre: str
    abstentions: str
    nonVotantsVolontaires: str

    @classmethod
    def from_json(cls, data: dict) -> Self:
        ref: str = data["scrutin"]["numero"]
        titre: str = data["scrutin"]["titre"]
        dateScrutin: str = data["scrutin"]["dateScrutin"]
        sort: str = data["scrutin"]["sort"]["code"]
        nombreVotants: str = data["scrutin"]["syntheseVote"]["nombreVotants"]
        nonVotants: str = data["scrutin"]["syntheseVote"]["decompte"]["nonVotants"]
        pour: str = data["scrutin"]["syntheseVote"]["decompte"]["pour"]
        contre: str = data["scrutin"]["syntheseVote"]["decompte"]["contre"]
        abstentions: str = data["scrutin"]["syntheseVote"]["decompte"]["abstentions"]
        nonVotantsVolontaires: str = data["scrutin"]["syntheseVote"]["decompte"]["nonVotantsVolontaires"]

        return cls(
            ref=ref,
            titre=titre,
            dateScrutin=dateScrutin,
            sort=sort,
            nombreVotants=nombreVotants,
            nonVotants=nonVotants,
            pour=pour,
            contre=contre,
            abstentions=abstentions,
            nonVotantsVolontaires=nonVotantsVolontaires,
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
            Non votants: {self.nonVotants}.\n                           \
            Pour: {self.pour}.\nContre: {self.contre}.\n                \
            Abstentions: {self.abstentions}.\n                          \
            Non votants volontaires: {self.nonVotantsVolontaires}."
    
    def to_string_depute(self, depute: Depute, res: str) -> str:
        return f"{depute.to_string_less()}\na voté **{res}** lors du \n{self.dateScrutin}, {self.sort}:\n{self.titre}"