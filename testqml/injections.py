# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import tempfile
from pathlib import Path

import inject
from PySide6.QtCore import QObject

from mpvqc.injections import bindings as original_bindings
from mpvqc.services import HostIntegrationService, SettingsService, WindowPropertiesService


class WindowPropertiesServiceOverride(WindowPropertiesService):
    def __init__(self) -> None:
        QObject.__init__(self)
        self._width = 0
        self._height = 0
        self._is_fullscreen = False
        self._is_maximized = False


class HostIntegrationServiceOverride(HostIntegrationService):
    def __init__(self) -> None:
        super().__init__(detect_configuration=False)


class SettingsServiceOverride(SettingsService):
    def __init__(self) -> None:
        directory = Path(tempfile.mkdtemp(prefix="mpvqc-qmltest-"))
        super().__init__(ini_file=str(directory / "settings.ini"))


def configure_injections() -> None:
    def test_bindings(binder: inject.Binder) -> None:
        original_bindings(binder)
        binder.bind_to_constructor(HostIntegrationService, HostIntegrationServiceOverride)
        binder.bind_to_constructor(SettingsService, SettingsServiceOverride)
        binder.bind_to_constructor(WindowPropertiesService, WindowPropertiesServiceOverride)

    inject.configure(test_bindings, bind_in_runtime=False, clear=True, allow_override=True)
