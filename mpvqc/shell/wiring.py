# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import inject


def bindings(binder: inject.Binder) -> None:
    import inject

    from mpvqc.services import SettingsFileService
    from mpvqc.shell.services import QuitService, ShellSettingsService

    def shell_settings_service() -> ShellSettingsService:
        return ShellSettingsService(inject.instance(SettingsFileService).qsettings)

    binder.bind_to_constructor(QuitService, QuitService)
    binder.bind_to_constructor(ShellSettingsService, shell_settings_service)


def register_qml_types() -> None:
    import mpvqc.shell.enums  # ruff: ignore[unused-import]
