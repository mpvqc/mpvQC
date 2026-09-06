# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import inject


def bindings(binder: inject.Binder) -> None:
    import inject
    from PySide6.QtCore import QSettings

    from mpvqc.shell.services import QuitService, ShellSettingsService, VersionCheckerService

    def shell_settings_service() -> ShellSettingsService:
        return ShellSettingsService(inject.instance(QSettings))

    binder.bind_to_constructor(QuitService, QuitService)
    binder.bind_to_constructor(ShellSettingsService, shell_settings_service)
    binder.bind_to_constructor(VersionCheckerService, VersionCheckerService)


def register_qml_types() -> None:
    import mpvqc.shell.enums  # ruff: ignore[unused-import]
    import mpvqc.shell.models  # ruff: ignore[unused-import]
    import mpvqc.shell.viewmodels  # ruff: ignore[unused-import]
