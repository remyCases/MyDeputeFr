# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from typing import Any, TypeAlias, TypeVar

from discord.ext.commands import Context, Cog
from typing_extensions import ParamSpec

P = ParamSpec("P")
T = TypeVar("T")
ContextT = TypeVar("ContextT", bound="Context[Any]")
CogT = TypeVar("CogT", bound="Cog")

JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None
