# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject

import mpvqc.services as s
from mpvqc.appearance import bindings as appearance_bindings
from mpvqc.comments import bindings as comments_bindings
from mpvqc.exporting import bindings as exporting_bindings
from mpvqc.i18n import bindings as i18n_bindings
from mpvqc.importing import bindings as importing_bindings
from mpvqc.player import bindings as player_bindings
from mpvqc.window import bindings as window_bindings


def _settings_service() -> s.SettingsService:
    return s.SettingsService(inject.instance(s.SettingsFileService).qsettings)


def bindings(binder: inject.Binder) -> None:
    appearance_bindings(binder)
    comments_bindings(binder)
    exporting_bindings(binder)
    i18n_bindings(binder)
    importing_bindings(binder)
    player_bindings(binder)
    window_bindings(binder)

    binder.bind_to_constructor(s.ApplicationPathsService, s.ApplicationPathsService)
    binder.bind_to_constructor(s.DesktopService, s.DesktopService)
    binder.bind_to_constructor(s.FileStartupService, s.FileStartupService)
    binder.bind_to_constructor(s.FontLoaderService, s.FontLoaderService)
    binder.bind_to_constructor(s.LabelWidthCalculatorService, s.LabelWidthCalculatorService)
    binder.bind_to_constructor(s.QuitService, s.QuitService)
    binder.bind_to_constructor(s.ResourceService, s.ResourceService)
    binder.bind_to_constructor(s.SettingsFileService, s.SettingsFileService)
    binder.bind_to_constructor(s.SettingsService, _settings_service)
    binder.bind_to_constructor(s.StateService, s.StateService)
    binder.bind_to_constructor(s.TimeFormatterService, s.TimeFormatterService)
    binder.bind_to_constructor(s.VersionCheckerService, s.VersionCheckerService)


def configure_injections() -> None:
    inject.configure(bindings, bind_in_runtime=False, clear=True)
