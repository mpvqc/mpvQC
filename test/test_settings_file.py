# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from unittest.mock import MagicMock

import inject
from PySide6.QtCore import QSettings

from mpvqc.injections import bindings
from mpvqc.services import ApplicationPathsService
from mpvqc.settings import open_settings_file


def test_opens_the_given_path_in_ini_format(tmp_path):
    path = tmp_path / "settings.ini"
    settings = open_settings_file(path)

    assert Path(settings.fileName()) == path
    assert settings.format() == QSettings.Format.IniFormat


def test_bindings_share_one_handle_at_the_application_settings_path(tmp_path):
    paths = MagicMock(spec_set=ApplicationPathsService)
    paths.file_settings = tmp_path / "settings.ini"

    def test_bindings(binder: inject.Binder) -> None:
        bindings(binder)
        binder.bind(ApplicationPathsService, paths)

    inject.configure(test_bindings, allow_override=True, bind_in_runtime=False)

    settings = inject.instance(QSettings)

    assert Path(settings.fileName()) == paths.file_settings
    assert inject.instance(QSettings) is settings
