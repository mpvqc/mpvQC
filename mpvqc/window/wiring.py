# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import inject


def bindings(binder: inject.Binder) -> None:
    from mpvqc.window.services import PlatformService

    binder.bind_to_constructor(PlatformService, PlatformService)


def register_qml_types() -> None:
    """The slice owns no QML-registered type yet; the window view models still sit in the layer packages."""
