# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject

from mpvqc.importing.services import ImporterService, ImportSettingsService, MimetypeProviderService
from mpvqc.services import SettingsFileService


def _import_settings_service() -> ImportSettingsService:
    return ImportSettingsService(inject.instance(SettingsFileService).qsettings)


def bindings(binder: inject.Binder) -> None:
    binder.bind_to_constructor(ImporterService, ImporterService)
    binder.bind_to_constructor(ImportSettingsService, _import_settings_service)
    binder.bind_to_constructor(MimetypeProviderService, MimetypeProviderService)
