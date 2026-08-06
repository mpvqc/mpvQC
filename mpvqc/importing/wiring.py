# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import inject


def bindings(binder: inject.Binder) -> None:
    import inject

    from mpvqc.importing.services import ImporterService, ImportSettingsService, MimeTypeProviderService
    from mpvqc.services import SettingsFileService

    def import_settings_service() -> ImportSettingsService:
        return ImportSettingsService(inject.instance(SettingsFileService).qsettings)

    binder.bind_to_constructor(ImporterService, ImporterService)
    binder.bind_to_constructor(ImportSettingsService, import_settings_service)
    binder.bind_to_constructor(MimeTypeProviderService, MimeTypeProviderService)


def register_qml_types() -> None:
    import mpvqc.importing.enums  # ruff: ignore[unused-import]
    import mpvqc.importing.models  # ruff: ignore[unused-import]
    import mpvqc.importing.viewmodels  # ruff: ignore[unused-import]
