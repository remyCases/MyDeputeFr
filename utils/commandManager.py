# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

from __future__ import annotations

from typing import Any, Callable, ClassVar, Self, TYPE_CHECKING
from discord import app_commands
from discord.ext.commands import Context, core, _types
from discord.ext.commands.hybrid import HybridCommand, CogT, P, T
from discord.utils import MISSING

from utils.cogManager import not_updating

if TYPE_CHECKING:
    from discord.ext.commands.hybrid import CommandCallback

class ProtectedCommand(HybridCommand[CogT, P, T]):
    """A class that is a protected during updates version of hybrid commands."""
    __commands_is_hybrid__: ClassVar[bool] = True

    def __init__(
        self: Self,
        func: CommandCallback[CogT, Context[Any], P, T],
        /,
        *,
        name: str | app_commands.locale_str = MISSING,
        description: str | app_commands.locale_str = MISSING,
        **kwargs: Any,
    ) -> None:
        super().__init__(not_updating()(func),
                         name=name,
                         description=description,
                         **kwargs)

def protected_command(
    name: str | app_commands.locale_str = MISSING,
    *,
    with_app_command: bool = True,
    **attrs: Any,
) -> Callable[[CommandCallback[CogT, _types.ContextT, P, T]], ProtectedCommand[CogT, P, T]]:
    """
    A decorator that transforms a function into a :class:`.ProtectedCommand`.

    Parameters
    -----------
    name: Union[:class:`str`, :class:`~discord.app_commands.locale_str`]
        The name to create the command with. By default this uses the
        function name unchanged.
    with_app_command: :class:`bool`
        Whether to register the command also as an application command.
    **attrs
        Keyword arguments to pass into the construction of the
        hybrid command.

    Raises
    -------
    TypeError
        If the function is not a coroutine or is already a command.
    """

    def decorator(func: CommandCallback[CogT, _types.ContextT, P, T]) -> ProtectedCommand[CogT, P, T]:
        if isinstance(func, core.Command):
            raise TypeError("Callback is already a command.")
        return ProtectedCommand(func,
                                name=name,
                                with_app_command=with_app_command,
                                **attrs)
    return decorator
