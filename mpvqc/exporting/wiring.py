# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import inject


def bindings(binder: inject.Binder) -> None:
    import inject

    from mpvqc.exporting.services import ExportService, ExportSettingsService
    from mpvqc.services import SettingsFileService

    def export_settings_service() -> ExportSettingsService:
        return ExportSettingsService(inject.instance(SettingsFileService).qsettings)

    binder.bind_to_constructor(ExportService, ExportService)
    binder.bind_to_constructor(ExportSettingsService, export_settings_service)


def register_qml_types() -> None:
    pass
