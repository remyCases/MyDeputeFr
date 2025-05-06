# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from typing import Any, Collection, Dict, List, TypeVar, Union

from discord.ext.commands import Context, Cog
from typing_extensions import ParamSpec

P = ParamSpec("P")
T = TypeVar("T")
ContextT = TypeVar("ContextT", bound="Context[Any]")
CogT = TypeVar("CogT", bound="Cog")

# TODO remove it by using Pedantic schema
JSON_DEPUTE = Dict[str, Dict[str, Union[
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