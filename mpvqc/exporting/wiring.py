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

    from mpvqc.exporting.services import ExportService, ExportSettingsService, ExportTemplateCatalogService

    def export_settings_service() -> ExportSettingsService:
        return ExportSettingsService(inject.instance(QSettings))

    binder.bind_to_constructor(ExportService, ExportService)
    binder.bind_to_constructor(ExportSettingsService, export_settings_service)
    binder.bind_to_constructor(ExportTemplateCatalogService, ExportTemplateCatalogService)


def register_qml_types() -> None:
    import mpvqc.exporting.models  # ruff: ignore[unused-import]
    import mpvqc.exporting.viewmodels  # ruff: ignore[unused-import]
