# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import inject


def bindings(binder: inject.Binder) -> None:
    from mpvqc.window.services import MainWindowService, PlatformService

    binder.bind_to_constructor(MainWindowService, MainWindowService)
    binder.bind_to_constructor(PlatformService, PlatformService)


def register_qml_types() -> None:
    import mpvqc.window.viewmodels  # ruff: ignore[unused-import]
