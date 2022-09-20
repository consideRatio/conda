# Copyright (C) 2012 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause
from __future__ import annotations

import pluggy

from typing import Callable, NamedTuple
from collections.abc import Iterable


_hookspec = pluggy.HookspecMarker("conda")
register = pluggy.HookimplMarker("conda")


class CondaSubcommand(NamedTuple):
    """
    Conda subcommand entry.

    :param name: Subcommand name (e.g., ``conda my-subcommand-name``).
    :param summary: Subcommand summary, will be shown in ``conda --help``.
    :param action: Callable that will be run when the subcommand is invoked.
    """
    name: str
    summary: str
    action: Callable[
        [list[str]],  # arguments
        int | None,  # return code
    ]


@_hookspec
def conda_subcommands() -> Iterable[CondaSubcommand]:
    """
    Register external subcommands in conda.

    :return: An iterable of subcommand entries.
    """
    ...

class CondaVirtualPackage(NamedTuple):
    """
    Conda subcommand entry.

    :param name: Virtual package name (e.g., ``my_custom_os``).
    :param version: Virtual package version (e.g., ``1.2.3``).
    """
    name: str
    version: Optional[str]


@_hookspec
def conda_virtual_package_plugin() -> Iterable[CondaVirtualPackage]:
    """
    Register virtual packages in Conda.

    :return: An iterable of virtual package entries.
    """
