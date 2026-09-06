# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QSettings

import mpvqc.services as s
from mpvqc.appearance import bindings as appearance_bindings
from mpvqc.comments import bindings as comments_bindings
from mpvqc.exporting import bindings as exporting_bindings
from mpvqc.i18n import bindings as i18n_bindings
from mpvqc.importing import bindings as importing_bindings
from mpvqc.player import bindings as player_bindings
from mpvqc.settings import open_settings_file
from mpvqc.shell import bindings as shell_bindings
from mpvqc.window import bindings as window_bindings


def bindings(binder: inject.Binder) -> None:
    def qsettings() -> QSettings:
        return open_settings_file(inject.instance(s.ApplicationPathsService).file_settings)

    appearance_bindings(binder)
    comments_bindings(binder)
    exporting_bindings(binder)
    i18n_bindings(binder)
    importing_bindings(binder)
    player_bindings(binder)
    shell_bindings(binder)
    window_bindings(binder)

    binder.bind_to_constructor(s.ApplicationPathsService, s.ApplicationPathsService)
    binder.bind_to_constructor(s.FileStartupService, s.FileStartupService)
    binder.bind_to_constructor(QSettings, qsettings)
    binder.bind_to_constructor(s.StateService, s.StateService)


def configure_injections() -> None:
    inject.configure(bindings, bind_in_runtime=False, clear=True)
