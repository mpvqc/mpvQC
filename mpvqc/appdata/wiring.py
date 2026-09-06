# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import inject


def bindings(binder: inject.Binder) -> None:
    from mpvqc.appdata.services import ApplicationPathsService

    binder.bind_to_constructor(ApplicationPathsService, ApplicationPathsService)


def register_qml_types() -> None:
    pass
